from cProfile import label
import sys
from os import getcwd
from PyQt6.QtCore import Qt, pyqtBoundSignal
from PyQt6 import uic,QtWidgets
from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QFrame, QMainWindow, QPushButton, QSpinBox, QVBoxLayout, QWidget,QDialog, QLabel, QFileDialog

from src.app.utils.resources import resource_path
import cv2

UI_FILE_PATH = resource_path("app.ui")

class CamaraIU(QMainWindow):
    def __init__(self):
        super().__init__()

        try:
            uic.loadUi(UI_FILE_PATH, self)
            print(f"Archivo '{UI_FILE_PATH}' cargado exitosamente.")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{UI_FILE_PATH}'")
            sys.exit(1)
        pantalla = QApplication.primaryScreen()
        geometria = pantalla.availableGeometry() # Excluye barras de herramientas

        self.ancho = geometria.width()
        self.alto = geometria.height()
        print(f"Resolución de pantalla: {self.ancho}x{self.alto}")
        # Ajustar al 80% de la resolución detectada
        self.resize(int(self.ancho * 0.8), int(self.alto * 0.9))

        # Centrar la ventana
        rect = self.frameGeometry()
        centro = geometria.center()
        rect.moveCenter(centro)
        self.move(rect.topLeft())
        self.initUI()
    def initUI(self):
        #Controles para la altura y acho de la imagen
        self.spin_alto = self.findChild(QSpinBox, "spin_alto")
        self.spin_alto.setRange(1, 10000)  # Establece un rango para el spinbox
        self.spin_alto.valueChanged.connect(self.cambio_alto)

        self.spin_ancho = self.findChild(QSpinBox, "spin_ancho")
        self.spin_ancho.setRange(1, 10000)  # Establece un rango para el spinbox
        self.spin_ancho.valueChanged.connect(self.cambio_ancho)

        self.frame_content = self.findChild(QFrame, "frame_content")
        self.frame_content.setMaximumSize(int(self.ancho * 0.3), int(self.alto * 0.4))  # Establece un tamaño mínimo para el frame de contenido
        # print(f"Tamaño máximo del frame de contenido: {self.frame_content.width()}x{self.frame_content.maximumHeight()}")
        #Label para cargar la imagen
        self.lbl_img = self.findChild(QLabel, "lbl_img")
        self.lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.lbl_img.setScaledContents(True)
        # Ruta de la imagen
        image_path = resource_path("src/assests/image.jpg")
        self.pixmap = QPixmap()
        self.q_image = QImage()



        self.leer_imagenes(image_path)




    def leer_imagenes(self,ruta):
        image_bgr = cv2.imread(ruta)

        if image_bgr is None:
            self.label_imagen.setText("No se pudo cargar la imagen.")
            return
        #Cambiamos el formato de BGR a RGB
        image_rgb =cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        # D. CONVERSIÓN A PYQT: Obtener dimensiones y mapear los bytes
        self.alto_real, self.ancho_real, canales = image_rgb.shape
        bytes_por_linea = canales * self.ancho_real


        self.q_image = QImage(
            image_rgb.data,
            self.ancho_real,
            self.alto_real,
            bytes_por_linea,
            QImage.Format.Format_RGB888
        )
        self.q_image_original = self.q_image.copy()  # Guardamos una copia original para futuras escalas
        self.spin_alto.setValue(self.alto_real)
        self.spin_ancho.setValue(self.ancho_real)
        self.pixmap =  QPixmap.fromImage(self.q_image)
        self.lbl_img.setPixmap(self.pixmap)
        pass


    def cambio_alto(self,value):
        print(f"Cambiando alto a: {value}")
        imagen_escalada = self.q_image_original.scaled(
            self.spin_ancho.value(), # Ancho actual del spinbox de ancho
            value,                   # El nuevo alto que viene del slider/spinbox
            Qt.AspectRatioMode.IgnoreAspectRatio, # Usa Ignore si quieres que obedezca EXACTAMENTE a los dos spinbox
            Qt.TransformationMode.SmoothTransformation # Para que no se vea pixelada
        )

        # 3. Actualizar el pixmap y mostrar
        self.pixmap = QPixmap.fromImage(imagen_escalada)
        self.lbl_img.setPixmap(self.pixmap)


    def cambio_ancho(self,value):
        print(f"Cambiando ancho a: {value}")
        imagen_escalada = self.q_image_original.scaled(
            value,                   # El nuevo anchoj
            self.spin_alto.value(),  # El alto actual del spinbox de alto
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.pixmap = QPixmap.fromImage(imagen_escalada)
        self.lbl_img.setPixmap(self.pixmap)


    def resizeEvent(self, event):
        """Este evento adapta la imagen al contenedor al cambiar el tamaño de la ventana"""
        super().resizeEvent(event)

        if hasattr(self, 'q_image_original') and not self.q_image_original.isNull():
            # 1. Obtener el tamaño disponible en el contenedor
            ancho_contenedor = self.frame_content.width()
            alto_contenedor = self.frame_content.height()

            # 2. Escalar la imagen manteniendo el aspecto para el contenedor
            imagen_escalada = self.q_image_original.scaled(
                int(self.ancho * 0.3),
                int(self.alto * 0.4),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            # 3. ¡ESTA ES LA CLAVE! Bloqueamos temporalmente las señales de los spinboxes
            # para que al cambiar sus valores aquí, no se vuelvan a disparar 'cambio_alto' o 'cambio_ancho'
            self.spin_alto.blockSignals(True)
            self.spin_ancho.blockSignals(True)
            
            # # Ponemos en los spinboxes el tamaño real que tomó la imagen adaptada
            self.spin_alto.setValue(imagen_escalada.height())
            self.spin_ancho.setValue(imagen_escalada.width())
            
            self.spin_alto.blockSignals(False)
            self.spin_ancho.blockSignals(False)

            # 4. Mostrar en la interfaz
            pixmap = QPixmap.fromImage(imagen_escalada)
            self.lbl_img.setPixmap(pixmap)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CamaraIU()
    window.show()
    sys.exit(app.exec())