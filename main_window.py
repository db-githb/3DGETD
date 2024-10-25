from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QScrollArea, QGridLayout
)
import sys
from random import randint
from generate_gaussians import GaussianGenerator


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Gaussian Generator")
        self.cam_widget = None
        self.gauss_widget = None
        layout = QVBoxLayout()
        cam_button = QPushButton("Create Cameras")
        cam_button.clicked.connect(self.show_new_window)
        layout.addWidget(cam_button)

        gauss_button = QPushButton("Generate Gaussians")
        gauss_button.clicked.connect(self.show_gauss_window)
        layout.addWidget(gauss_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_new_window(self):
        if self.cam_widget is None:
            self.cam_widget = AnotherWindow()
        self.cam_widget.show()
    
    def show_gauss_window(self):
        if self.gauss_widget is None:
            self.gauss_widget = GaussianGenerator()   
        self.gauss_widget.show()
        
app = QApplication(sys.argv)
widget = MainWindow()
widget.show()
app.exec()