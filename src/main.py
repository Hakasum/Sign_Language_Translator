import cv2
import time
import yaml
from src.detection import load_model, detect, load_config
from src.utils import filter_detections
from supervision import ByteTrack, BoxAnnotator, LabelAnnotator


config = load_config()

# === CONFIG ===
MODEL_PATH = config["model_path"]
SPACE_SIGN = config["space_sign"]
DELETE_SIGN = config["delete_sign"]
CONFIDENCE_THRESHOLD = config["confidence_threshold"]
DEFAULT_HOLD_TIME = config["default_hold_time"]
FUNCTIONAL_HOLD_TIME = config["functional_hold_time"]
COOLDOWN_TIME = config["cooldown_time"]
MAX_DETECTIONS = config["max_detections"]

# === INIT ===
model = load_model(MODEL_PATH)
tracker = ByteTrack()
box_annotator = BoxAnnotator()
label_annotator = LabelAnnotator()

font = cv2.FONT_HERSHEY_TRIPLEX
font_color = (0, 128, 255)
thickness = 2

tracked_signs = {}
sentence = ""

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    current_time = time.time()
    results = detect(model, frame)
    detections = filter_detections(results, CONFIDENCE_THRESHOLD, MAX_DETECTIONS)
    tracked_detections = tracker.update_with_detections(detections)

    labels = []

    for box, class_id, track_id in zip(
        tracked_detections.xyxy,
        tracked_detections.class_id,
        tracked_detections.tracker_id
    ):
        sign = model.names[class_id]
        labels.append(f"{sign} #{track_id}")

        if track_id not in tracked_signs:
            tracked_signs[track_id] = {
                "sign": sign,
                "start": current_time,
                "last_sign": None,
                "last_added": 0,
                "delete_count": 0
            }

        state = tracked_signs[track_id]

        if state["sign"] == sign:
            hold_duration = current_time - state["start"]

            if sign == DELETE_SIGN:
                if state["delete_count"] >= 2:
                    adjusted_hold = FUNCTIONAL_HOLD_TIME / ((state["delete_count"] / 2) + 1)
                else:
                    adjusted_hold = FUNCTIONAL_HOLD_TIME

                if hold_duration >= adjusted_hold and len(sentence) > 0:
                    sentence = sentence[:-1]
                    state["delete_count"] += 1
                    state["start"] = current_time

            else:
                if hold_duration >= DEFAULT_HOLD_TIME:
                    if (
                        state["last_sign"] != sign or
                        current_time - state["last_added"] >= COOLDOWN_TIME
                    ):
                        if sign == SPACE_SIGN:
                            sentence += " "
                        else:
                            sentence += sign

                        state["last_sign"] = sign
                        state["last_added"] = current_time
                        state["start"] = current_time
                        state["delete_count"] = 0

        else:
            state["sign"] = sign
            state["start"] = current_time
            if sign != DELETE_SIGN:
                state["delete_count"] = 0

    annotated_frame = box_annotator.annotate(scene=frame.copy(), detections=tracked_detections)
    annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=tracked_detections, labels=labels)

    for box, confidence in zip(tracked_detections.xyxy, tracked_detections.confidence):
        x1, y1, x2, y2 = map(int, box)
        conf_text = f"{confidence:.2f}"
        text_size, _ = cv2.getTextSize(conf_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 1)
        text_x = x1
        text_y = y2 + text_size[1] + 5
        cv2.putText(annotated_frame, conf_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    cursor_visible = int(time.time() * 2) % 2 == 0
    displayed_sentence = sentence + ("|" if cursor_visible else "")
    cv2.putText(annotated_frame, f"Sentence: {displayed_sentence}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Sign Detector with Tracking", annotated_frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()