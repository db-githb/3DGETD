from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QScrollArea, QGridLayout
)
import sys
from generate_gaussians import GaussianGenerator
from create_cameras import CreateCameras


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Gaussian Generator")
        self.cam_widget = None
        self.gauss_widget = None
        layout = QVBoxLayout()
        cam_button = QPushButton("Create Cameras")
        cam_button.clicked.connect(self.show_cam_window)
        layout.addWidget(cam_button)

        gauss_button = QPushButton("Generate Gaussians")
        gauss_button.clicked.connect(self.show_gauss_window)
        layout.addWidget(gauss_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_cam_window(self):
        if self.cam_widget is None:
            self.cam_widget = CreateCameras()
        self.cam_widget.show()
    
    def show_gauss_window(self):
        if self.gauss_widget is None:
            self.gauss_widget = GaussianGenerator()   
        self.gauss_widget.show()
        
app = QApplication(sys.argv)
widget = MainWindow()
widget.show()
app.exec()