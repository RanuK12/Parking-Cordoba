# Especificación Técnica y de Negocio — Parking Córdoba

## Modelo de Negocio
- **Objetivo**: Sistema de estacionamiento en tiempo real para Córdoba con visión por computadora.
- **Ingresos**: Suscripción para estacionamientos + API para apps de usuarios.
- **Piloto**: 2 zonas de Córdoba.

## Arquitectura Técnica
- **Stack**: Python, OpenCV/YOLOv8, FastAPI.
- **Arquitectura**: Edge device → Cloud.
- **Métricas de éxito**: Latencia <2s, precisión >90%.

## Roadmap
1. **Fase 1**: Detección de vehículos (prototipo funcional).
2. **Fase 2**: API REST para integración con apps de usuarios.
3. **Fase 3**: App móvil para conductores.