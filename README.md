# parking-cordoba

Sistema de estacionamiento en tiempo real para la ciudad de Córdoba con visión por computadora.

## Objetivo del producto

Detectar plazas de estacionamiento libres u ocupadas en tiempo real a partir de cámaras de video, exponiendo los datos mediante una API REST para que conductores y el municipio sepan dónde hay lugar disponible sin dar vueltas.

## Documento maestro (spec técnica + negocio + piloto)

### 1. Stack tecnológico

- **Detección**: Python + OpenCV + YOLOv8 (ultralytics) para detectar vehículos en cada frame.
- **API REST**: FastAPI (endpoints `/plazas`, `/estado/<zona>`, `/health`).
- **Video**: captura desde RTSP o archivo de prueba local.
- **Despliegue piloto**: Docker + docker-compose (cámara → contenedor de detección → API).

### 2. Prototipo funcional (detect_parking.py)

Script que recibe una imagen o video de entrada, detecta vehículos con YOLOv8, dibuja bounding boxes y guarda el resultado en `output.jpg`. Correr con un solo comando:

```bash
python detect_parking.py --input prueba.jpg --output output.jpg
```

### 3. Modelo de negocio

- **Diferencial clave**: datos de ocupación en tiempo real vía visión por computadora (las apps existentes muestran mapas desactualizados).
- **Ingresos**: suscripción B2B a parkings privados y municipios; API de datos para apps de terceros.
- **Piloto**: una zona piloto en Córdoba (ej. centro o Nueva Córdoba) con 2-3 cámaras, validando precisión de detección vs. conteo manual durante 2 semanas.

### 4. Hoja de ruta

1. ✅ Prototipo de detección con una imagen (detect_parking.py).
2. API REST con FastAPI exponiendo estado de plazas.
3. Integración con video RTSP en tiempo real.
4. Piloto en zona real de Córdoba con métricas de precisión.
5. App móvil/web para conductores.

## Estado actual

- `detect_parking.py`: prototipo base de detección de vehículos con YOLOv8 + OpenCV.
- `docs/mercado.md`: análisis de competencia y oportunidad de mercado en Córdoba.
- Próximo: API REST y despliegue Docker.
