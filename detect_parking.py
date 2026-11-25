import cv2
import numpy as np
from ultralytics import YOLO
import argparse
import json
import os
import sys

# IDs de clase COCO que son vehículos (relevantes para estacionamiento)
VEHICLE_CLASSES = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}

# Cargar modelo YOLO preentrenado
try:
    model = YOLO('yolov8n.pt')
except Exception as exc:
    print(f'Error: no se pudo cargar el modelo YOLO: {exc}', file=sys.stderr)
    sys.exit(1)


def detect_parking_spaces(frame):
    """Detecta vehículos en un frame y devuelve bboxes ocupados y detecciones."""
    results = model(frame)
    boxes = results[0].boxes

    occupied = []
    detections = []
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        detections.append({
            'class': VEHICLE_CLASSES.get(cls_id, str(cls_id)),
            'confidence': round(conf, 2),
            'bbox': [int(x1), int(y1), int(x2), int(y2)],
        })
        # Solo las clases de vehículo cuentan como espacio ocupado
        if cls_id in VEHICLE_CLASSES:
            occupied.append((int(x1), int(y1), int(x2), int(y2)))

    return occupied, detections


def annotate_frame(frame, occupied):
    for (x1, y1, x2, y2) in occupied:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return frame


def process_video(video_path, output_path, json_out_path=None, display=True):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f'Error: no se pudo abrir el video: {video_path}', file=sys.stderr)
        sys.exit(1)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    all_detections = []
    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        occupied, detections = detect_parking_spaces(frame)
        all_detections.append({
            'frame': frame_idx,
            'occupied': len(occupied),
            'detections': detections,
        })
        annotate_frame(frame, occupied)

        out.write(frame)
        if display:
            cv2.imshow('Parking Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        frame_idx += 1

    cap.release()
    out.release()
    if display:
        cv2.destroyAllWindows()

    if json_out_path:
        with open(json_out_path, 'w', encoding='utf-8') as f:
            json.dump({'frames': all_detections}, f, ensure_ascii=False, indent=2)

    return all_detections


def process_image(image_path, output_path, json_out_path=None, display=True):
    frame = cv2.imread(image_path)
    if frame is None:
        print(f'Error: no se pudo leer la imagen: {image_path}', file=sys.stderr)
        sys.exit(1)

    occupied, detections = detect_parking_spaces(frame)
    annotate_frame(frame, occupied)

    cv2.imwrite(output_path, frame)

    result = {'occupied': len(occupied), 'detections': detections}
    if json_out_path:
        with open(json_out_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    else:
        print(json.dumps(result, ensure_ascii=False))

    if display:
        cv2.imshow('Parking Detection', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return result


def main():
    parser = argparse.ArgumentParser(description='Detección de espacios de estacionamiento con YOLOv8')
    parser.add_argument('--input', required=True, help='Ruta al archivo de imagen o video')
    parser.add_argument('--output', default='output.mp4', help='Ruta de salida para video/imagen procesada')
    parser.add_argument('--json-out', dest='json_out', default=None, help='Guardar detecciones en JSON a este archivo')
    parser.add_argument('--no-display', dest='no_display', action='store_true', help='Modo headless: no mostrar ventanas')
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f'Error: el archivo de entrada no existe: {args.input}', file=sys.stderr)
        sys.exit(1)

    is_image = args.input.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp'))

    if is_image:
        process_image(args.input, args.output, args.json_out, display=not args.no_display)
    else:
        process_video(args.input, args.output, args.json_out, display=not args.no_display)


if __name__ == '__main__':
    main()
