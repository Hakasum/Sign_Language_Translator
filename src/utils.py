from supervision import Detections


def filter_detections(results, confidence_threshold, max_detections):
    detections = Detections.from_ultralytics(results)
    mask = detections.confidence >= confidence_threshold
    detections = detections[mask]

    sorted_indices = detections.confidence.argsort()[::-1]
    detections = detections[sorted_indices]

    return detections[:max_detections] if len(detections) > max_detections else detections