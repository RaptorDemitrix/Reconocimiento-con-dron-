import cv2
import threading
import time
import os
from datetime import datetime
from ultralytics import YOLO

class LectorVideo:
    """Maneja la recepción de video en un hilo separado para evitar lag."""
    def __init__(self, url):
        self.cap = cv2.VideoCapture(url)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) 
        self.frame = None
        self.corriendo = True
        
        if not self.cap.isOpened():
            print("Error: No se detecta la transmisión. Revisa el servidor RTMP.")
            self.corriendo = False
        else:
            self.hilo = threading.Thread(target=self._recibir_imagenes, daemon=True)
            self.hilo.start()
            print("Conexión de video establecida. Recibiendo frames...")

    def _recibir_imagenes(self):
        while self.corriendo:
            exito, frame = self.cap.read()
            if exito:
                self.frame = frame 
            else:
                self.corriendo = False
                print("Se perdió la conexión de video.")

    def detener(self):
        self.corriendo = False
        self.cap.release()


def guardar_captura(frame_anotado, carpeta="capturas_dron"):
    """
    Función NUEVA: Crea una carpeta (si no existe) y guarda la imagen 
    con un nombre único basado en la fecha y hora exacta.
    """
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
        
    # Crear un nombre de archivo único usando la fecha y hora
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ruta_archivo = f"{carpeta}/deteccion_{timestamp}.jpg"
    
    cv2.imwrite(ruta_archivo, frame_anotado)
    print(f"📸 ¡Objeto detectado! Captura guardada en: {ruta_archivo}")


def procesar_con_yolo(lector, modelo):
    """Toma el frame más reciente y lo procesa con YOLO."""
    print("Iniciando IA YOLOv26... Presiona 'q' para salir.")
    
    # Variables para controlar cada cuánto tiempo se guarda una captura
    tiempo_ultima_captura = 0
    cooldown_segundos = 2.0  # Espera 2 segundos antes de guardar otra foto
    
    while lector.corriendo:
        frame_actual = lector.frame
        
        if frame_actual is None:
            time.sleep(0.1)
            continue
            
        frame_a_procesar = frame_actual.copy()
        
        # Procesar con YOLO
        resultados = modelo(frame_a_procesar, conf=0.5, imgsz=320)
        
        # Dibujar resultados (las cajas de colores)
        frame_anotado = resultados[0].plot()
        
        # NUEVO: Lógica para guardar la imagen si detecta algo
        # len(resultados[0].boxes) nos dice cuántos objetos encontró
        if len(resultados[0].boxes) > 0:
            tiempo_actual = time.time()
            
            # Verifica si ya pasaron los segundos de espera estipulados
            if (tiempo_actual - tiempo_ultima_captura) > cooldown_segundos:
                guardar_captura(frame_anotado)
                tiempo_ultima_captura = tiempo_actual
        
        # Mostrar en pantalla
        cv2.imshow("DJI Mini 4K - Detección Multihilo", frame_anotado)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    lector.detener()
    cv2.destroyAllWindows()

# --- BLOQUE PRINCIPAL ---
if __name__ == "__main__":
    modelo_yolo = YOLO('yolo26n.pt')
    
    # Recuerda usar tu IP real
    url_rtmp = "rtmp://10.130.76.252/live/drone" 
    
    lector_dron = LectorVideo(url_rtmp)
    
    if lector_dron.corriendo:
        procesar_con_yolo(lector_dron, modelo_yolo)