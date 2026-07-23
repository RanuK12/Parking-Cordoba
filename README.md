# Parking-Cordoba

Sistema de detección de espacios de estacionamiento libres/ocupados usando computer vision (YOLO).

## Fase B3-F2: Prototipo de detección

Script que con YOLO sobre una imagen/video de prueba distingue espacios ocupados vs libres y lo muestra.

## Requisitos

- Python 3.8+
- ultralytics (YOLO)
- opencv-python
- numpy

## Instalación

```bash
pip install ultralytics opencv-python numpy
```

## Uso

```bash
python detect_parking.py --input test_parking.jpg
python detect_parking.py --input test_parking.mp4
```