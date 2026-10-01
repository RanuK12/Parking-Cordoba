# Especificación técnica preliminar - Sistema de estacionamiento en tiempo real para Córdoba

## Visión del producto
Aplicación móvil y web que muestra disponibilidad de cupos de estacionamiento en tiempo real en la ciudad de Córdoba, con notificaciones push para vencimientos y alertas de zonas liberadas.

## Prioridades técnicas
1. **API de cupos en tiempo real**
   - Integración con sensores existentes de la municipality (SEMM) o instalación de cámaras con visión por computadora en puntos clave
   - Endpoint REST/WebSocket para consultar disponibilidad por zona/cuadra
   - Caché de datos para reducir carga en sensores

2. **Notificaciones push**
   - Alertas de vencimiento inminente (5 min antes)
   - Notificaciones cuando se libera un cupo en zona favorita
   - Recordatorios de pago pendiente

3. **Experiencia de usuario**
   - Mapa interactivo con colores por disponibilidad (verde=disponible, rojo=lleno, amarillo=pocos)
   - Historial de estacionamientos y pagos
   - Integración con billeteras digitales (Mercado Pago, Ualá)

## Arquitectura propuesta
- Frontend: React Native (móvil) + React Web (admin/consulta)
- Backend: Node.js/Express o Python/FastAPI
- Base de datos: PostgreSQL + Redis para caché en tiempo real
- Servicios externos: Google Maps API, Firebase Cloud Messaging (push)

## Próximos pasos de validación
- Piloto en 2-3 zonas céntricas de Córdoba con 10-20 cámaras/test
- Validación de precisión con conteo manual vs detección automática
- Encuestas a usuarios potenciales sobre disposición a pagar