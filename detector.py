import cv2
from ultralytics import YOLO
import argparse


def detect_vehicles(image_path):
    """Detect vehicles in an image using YOLOv8 nano model.

    Returns a list of bounding boxes with class names and confidence scores.
    """
    model = YOLO('yolov8n.pt')
    results = model(image_path)
    detections = []
    for result in results:
        boxes = result.boxes
        if boxes is not None:
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()
                name = model.names[cls]
                # COCO classes 2-7 are vehicles: car, motorcycle, bus, train, truck
                if name in ('car', 'motorcycle', 'bus', 'train', 'truck'):
                    detections.append({
                        'class': name,
                        'confidence': conf,
                        'bbox': xyxy,
                    })
    return detections


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect vehicles in an image.')
    parser.add_argument('--image', type=str, required=True, help='Path to the image file.')
    args = parser.parse_args()

    detections = detect_vehicles(args.image)
    for d in detections:
        print(f"{d['class']}: conf={d['confidence']:.2f} bbox={d['bbox']}")