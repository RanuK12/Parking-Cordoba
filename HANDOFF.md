# Parking-Cordoba — HANDOFF

## Estado actual (B3-F2)
- [x] Script `detect_parking.py` con YOLOv8 para detectar espacios ocupados vs libres
- [x] `requirements.txt` con dependencias
- [x] `README.md` con instrucciones de instalación y uso
- [ ] Imagen/video de prueba real (se necesita un parking de Córdoba)
- [ ] Ajuste fino del modelo con imágenes reales del parking objetivo

## Cómo probarlo
```bash
pip install -r requirements.txt
python detect_parking.py --input test_image.jpg
```

## Próximos pasos (B3-F3)
- Conseguir imágenes reales del parking a monitorear
- Definir ROI (regiones de interés) para cada espacio de parking
- Ajustar umbrales de detección para el caso concreto
- Agregar contador de espacios libres/ocupados