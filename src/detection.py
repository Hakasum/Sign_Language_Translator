import yaml
from ultralytics import YOLO


def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_model(model_path):
    return YOLO(model_path)


def detect(model, frame):
    results = model(frame)[0]
    return results