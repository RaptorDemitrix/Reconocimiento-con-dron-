# Real-Time Drone Object Detection & Capture (YOLOv26)

Este proyecto permite la recepción y procesamiento de transmisiones de video en tiempo real vía **RTMP** (como el flujo de video de un dron DJI Mini 4K), realizando detección de objetos mediante modelos **YOLO** de Ultralytics con soporte multihilo para optimizar la latencia y evitar desfasamientos (lag).

Además, cuenta con una funcionalidad para guardar capturas de pantalla automáticas de las detecciones realizadas con una frecuencia de seguridad (*cooldown*).

---

## 🛠️ Características

- **Recepción Multihilo (`threading`):** La lectura de la transmisión RTMP corre en un hilo independiente para procesar siempre el cuadro (*frame*) más reciente del video y minimizar la acumulación de búfer.
- **Detección con YOLO:** Utiliza modelos YOLO de Ultralytics con filtrado de confianza personalizable.
- **Captura Automática:** Guarda automáticamente en la carpeta `capturas_dron/` cualquier cuadro donde se detecte un objeto, nombrando la imagen con fecha y hora exacta (`YYYY-MM-DD_HH-MM-SS.jpg`).
- **Cooldown de Capturas:** Previene la sobrecarga de imágenes guardando capturas con un intervalo de tiempo mínimo parametrizable (por defecto, 2 segundos).

---

## 📋 Requisitos Previos

Asegúrate de tener instalado Python 3.8 o superior. Instala las dependencias necesarias ejecutando:

```bash
pip install opencv-python ultralytics
```

---

## ⚙️ Configuración

Antes de ejecutar el script, edita el archivo `yolo26_1.py` si deseas ajustar alguno de los siguientes parámetros:

1. **Servidor RTMP:** Modifica la variable `url_rtmp` en el bloque principal con la dirección IP y ruta de tu transmisión:
   ```python
   url_rtmp = "rtmp://TU_DIRECCION_IP/live/drone"
   ```
2. **Modelo YOLO:** Cambia el modelo asignado en `modelo_yolo = YOLO('yolo26n.pt')` según tus necesidades (`yolov8n.pt`, `yolo11n.pt`, etc.).
3. **Umbral de Confianza e Intervalos:**
   - Ajusta `conf=0.5` o `imgsz=320` dentro de la llamada a `modelo()` para afinar el rendimiento.
   - Ajusta `cooldown_segundos = 2.0` para definir cada cuántos segundos se puede tomar una captura automática.

---

## 🚀 Uso

Ejecuta el script principal desde tu terminal:

```bash
python yolo26_1.py
```

- **Para salir:** Haz clic en la ventana de visualización y presiona la tecla `q`.

---

## 📁 Estructura del Proyecto

```text
.
├── yolo26_1.py            # Script principal de captura y detección
├── README.md              # Documentación del proyecto
└── capturas_dron/         # Carpeta generada automáticamente donde se guardan las detecciones
```

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT - siéntete libre de usarlo, modificarlo y distribuirlo según tus necesidades.