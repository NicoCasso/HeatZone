from ultralytics import YOLO

def load_model(model_path="models/yolov8n.pt"):
    return YOLO(model_path)
