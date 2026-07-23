import cv2
import numpy as np
from ultralytics import YOLO
import argparse

# Cargar modelo YOLO preentrenado
model = YOLO('yolov8n.pt')

def detect_parking_spaces(frame):
    # Preprocesamiento (ej: resize, normalización)
    results = model(frame)
    boxes = results[0].boxes  # Bounding boxes detectados
    
    occupied = []
    free = []
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        # Lógica para determinar si el espacio está ocupado (ej: tamaño del bbox)
        if (x2 - x1) * (y2 - y1) > 10000:  # Umbral arbitrario
            occupied.append((int(x1), int(y1), int(x2), int(y2)))
        else:
            free.append((int(x1), int(y1), int(x2), int(y2)))
    
    return occupied, free

def process_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        occupied, free = detect_parking_spaces(frame)
        for (x1, y1, x2, y2) in occupied:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        for (x1, y1, x2, y2) in free:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        out.write(frame)
        cv2.imshow('Parking Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Ruta al archivo de imagen/video')
    parser.add_argument('--output', default='output.mp4', help='Ruta de salida para video procesado')
    args = parser.parse_args()

    if args.input.endswith(('.jpg', '.png')):
        frame = cv2.imread(args.input)
        occupied, free = detect_parking_spaces(frame)
        for (x1, y1, x2, y2) in occupied:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        for (x1, y1, x2, y2) in free:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow('Parking Detection', frame)
        cv2.waitKey(0)
        cv2.imwrite('output.jpg', frame)
    else:
        process_video(args.input, args.output)

if __name__ == '__main__':
    main()
