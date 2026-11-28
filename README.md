# Parking Cordoba

Sistema de estacionamiento en tiempo real para Córdoba con visión por computadora.

## Features

- Detección de vehículos usando YOLOv8
- Exportación de resultados en formato JSON (--json-out)
- Interfaz de línea de comandos

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python detect_parking.py --input video.mp4 --output annotated.mp4 --json-out results.json
```

## Licencia

MIT