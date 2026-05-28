from cProfile import label
import sys
from os import getcwd
from PyQt6.QtCore import Qt, pyqtBoundSignal
from PyQt6 import uic,QtWidgets
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,QDialog, QLabel, QFileDialog

from src.app.utils.resources import resource_path

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
        self.initUI() 
    def initUI(self):

        self.lbl_img = self.findChild(QLabel, "lbl_img")
        image_path = resource_path("src/assests/image.jpg")
        print(f"Cargando imagen desde: {image_path}")
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error: no se pudo cargar la imagen '{image_path}'")
            return

        self.lbl_img.setPixmap(pixmap)
        self.lbl_img.setScaledContents(True)
        self.lbl_img.adjustSize()
        self.resize(pixmap.width(), pixmap.height())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CamaraIU()
    window.show()
    sys.exit(app.exec())