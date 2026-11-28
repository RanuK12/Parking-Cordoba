# Parking Córdoba — Documento Maestro (Spec Técnica + Negocio + Piloto)

**Proyecto:** parking-cordoba (RanuK12/parking-cordoba)
**Estado:** v1.0 — borrador inicial
**Autor:** Emilio Ranucoli / Ranuk IT Solutions

---

## 1. Visión del producto

Sistema de estacionamiento en tiempo real para la ciudad de Córdoba (Argentina) basado en visión por computadora. Detecta, a partir de cámaras instaladas sobre cada espacio de parking, si cada plaza está **libre u ocupada**, y expone esa información por una API para que conductores y operadores sepan dónde hay lugar disponible sin dar vueltas.

**Objetivo inmediato:** tener un documento maestro (esta spec) y un prototipo de detección que corra con un solo comando. Recién después, la app.

---

## 2. Especificación técnica

### 2.1 Alcance del prototipo (v1)

- Un script Python `detect_parking.py` que reciba un video o imagen de entrada y devuelva, por frame, la lista de espacios detectados con su estado (libre/ocupado) y su bounding box.
- Detección real de vehículos (no umbral arbitrario de tamaño de bbox).
- Salida: video anotado (rectángulos verdes = libre, rojos = ocupado) + JSON opcional con los resultados por frame.
- Ejecutable con un comando: `python detect_parking.py --input <video|imagen> --output <salida>`.

### 2.2 Stack

- Lenguaje: Python 3.10+
- Detección: YOLOv8 nano (`ultralytics`) — modelo `yolov8n.pt`, rápido y ligero, ideal para correr en CPU en la Mac de desarrollo.
- Procesamiento de video/imagen: OpenCV (`opencv-python`)
- CLI: `argparse`
- Serialización de salida: JSON (`json`, stdlib)

### 2.3 Dependencias

```
ultralytics
opencv-python
numpy
```

### 2.4 Arquitectura del prototipo

```
detect_parking.py
├── load_model()        -> carga yolov8n.pt una sola vez
├── detect_frame(frame) -> corre YOLO, filtra clases "car"/"truck"/"bus"/"motorcycle"
├── classify_spaces()   -> asigna cada vehículo a un espacio de parking (por IoU con zonas predefinidas o por clustering simple)
├── annotate(frame)     -> dibuja rectángulos: verde libre / rojo ocupado
├── process_video()     -> lee video frame a frame, escribe video de salida + JSON
└── main()              -> argparse --input / --output / --json
```

### 2.5 Formato de salida JSON (opcional)

```json
{
  "video": "entrada.mp4",
  "fps": 20.0,
  "frames": [
    {
      "frame": 0,
      "spaces": [
        {"id": 1, "bbox": [x1, y1, x2, y2], "estado": "libre"},
        {"id": 2, "bbox": [x1, y1, x2, y2], "estado": "ocupado"}
      ]
    }
  ]
}
```

---

## 3. Especificación de negocio

### 3.1 Problema

En Córdoba capital, encontrar estacionamiento en el centro y barrios cercanos es un dolor diario. Los conductores dan vueltas buscando lugar, generando tráfico extra, contaminación y tiempo perdido. No hay información pública en tiempo real de disponibilidad de plazas.

### 3.2 Solución

Red de cámaras baratas (una por grupo de plazas) + detección por visión por computadora + API que devuelve disponibilidad en tiempo real. El conductor consulta una app/mapa y va directo al lugar libre.

### 3.3 Mercado objetivo (piloto)

- Estacionamientos públicos y privados de superficie en Córdoba capital (centro, Nueva Córdoba, Güemes).
- Shopping centers y centros comerciales con parking propio.
- Municipalidad de Córdoba (datos abiertos de movilidad).

### 3.4 Modelo de ingresos (v1)

- Suscripción mensual a operadores de parking por acceso a la API de disponibilidad.
- Análisis de ocupación histórica (reportes de uso por franja horaria) vendidos a municipios y desarrolladores inmobiliarios.
- Integración con apps de navegación (Waze, Google Maps) — pago por lead o por consulta API.

### 3.5 Ventaja competitiva

- Visión por computadora sin sensores en el suelo (más barato de instalar y mantener que sensores magnéticos por plaza).
- Modelo YOLO nano: corre en hardware barato (Raspberry Pi, Jetson Nano, o una PC vieja).
- Enfoque local en Córdoba: conocimiento del terreno y velocidad de despliegue del piloto.

---

## 4. Plan de piloto (fase 1)

| Hito | Qué se hace | Entregable | Fecha tentativa |
|------|-------------|------------|-----------------|
| 1 | Documento maestro (esta spec) + prototipo de detección que corra con un comando | SPEC.md + detect_parking.py funcional | Semana 1 |
| 2 | Consegui video de muestra de un parking de Córdoba (YouTube / Drive / grabar) | video_test.mp4 | Semana 2 |
| 3 | Ejecutar prototipo sobre el video de muestra y validar detección libre/ocupado | video anotado + JSON de salida | Semana 3 |
| 4 | Exponer resultados por una API simple (FastAPI) | endpoint `/estado` | Semana 4 |
| 5 | Piloto real: 1 cámara + 10 plazas en un parking de Córdoba | dashboard en vivo | Mes 2 |

---

## 5. Criterios de éxito del prototipo

- [ ] `detect_parking.py` corre con `python detect_parking.py --input <archivo> --output <salida>` sin errores.
- [ ] Detecta vehículos reales (clases COCO: car, truck, bus, motorcycle), no por umbral de tamaño arbitrario.
- [ ] Genera video de salida anotado (rectángulos de color según estado).
- [ ] Opcionalmente genera JSON con los resultados por frame.
- [ ] Código limpio, con docstrings y sin dependencias innecesarias.

---

## 6. Próximos pasos (después del prototipo)

1. API con FastAPI que reciba un frame y devuelva estado de plazas en JSON.
2. Interfaz web simple (mapa de plazas libres/ocupadas en tiempo real).
3. Piloto con cámara física en un parking de Córdoba.
4. App móvil para conductores.

---

*Fin del documento maestro.*
