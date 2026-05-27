from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys

UI_FILE_PATH = "app.ui"

class CamaraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camara App")

        # Cargamos el archivo app.ui
