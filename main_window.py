import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QHBoxLayout, QMessageBox

from utils import openDirectoryDialog, toggleButtons, checkDirectoryValidity
from generate_gaussians import GaussianGenerator
from create_cameras import CreateCameras

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.widgetCam = None
        self.widgetGauss = None

        # Set up the main layout
        self.layout = QVBoxLayout()

        # Create a horizontal layout for the directory input field and button
        self.mainWindowLayout = QHBoxLayout()

        # Create a line edit for the user to type the directory
        self.pathEntry = QLineEdit(self)
        self.pathLabel = QLabel("Select Project Path:")
        self.pathEntry.returnPressed.connect(lambda: checkDirectoryValidity(self))
        self.pathEntry.textChanged.connect(lambda: toggleButtons(self))
        self.mainWindowLayout.addWidget(self.pathLabel)
        self.mainWindowLayout.addWidget(self.pathEntry)

        # Create a button to open the directory dialog
        self.browseButton = QPushButton('Browse', self)
        self.browseButton.clicked.connect(lambda: openDirectoryDialog(self))
        self.mainWindowLayout.addWidget(self.browseButton)

        # Add the directory input layout to the main layout
        self.layout.addLayout(self.mainWindowLayout)

        # Create an Enter button for the user to confirm the directory
        self.buttonEnter = QPushButton('Create Directory', self)
        self.buttonEnter.setEnabled(False)
        self.buttonEnter.clicked.connect(lambda: checkDirectoryValidity(self))
        self.layout.addWidget(self.buttonEnter)

        # Label to show the selected directory
        self.labelPath = QLabel('No directory selected', self)
        self.layout.addWidget(self.labelPath)

        # Option buttons (initially disabled)
        self.buttonCam = QPushButton('Create Cameras', self)
        self.buttonCam.setEnabled(False)
        self.buttonCam.clicked.connect(lambda: checkDirectoryValidity(self))
        self.buttonCam.clicked.connect(self.show_cam_window)
        self.layout.addWidget(self.buttonCam)

        self.buttonGauss = QPushButton('Generate Gaussians', self)
        self.buttonGauss.setEnabled(False)
        self.buttonGauss.clicked.connect(lambda: checkDirectoryValidity(self))
        self.buttonGauss.clicked.connect(self.show_gauss_window)
        self.layout.addWidget(self.buttonGauss)

        # Set the layout and window title
        self.setLayout(self.layout)
        self.setWindowTitle("3D Gaussian Generator")

    def show_cam_window(self):
        if self.widgetCam is None:
            self.widgetCam = CreateCameras(self.pathEntry)
        self.widgetCam.show()
    
    def show_gauss_window(self):
        if self.widgetGauss is None:
            self.widgetGauss = GaussianGenerator(self.pathEntry)   
        self.widgetGauss.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setMinimumSize(500, 100)
    window.show()
    sys.exit(app.exec_())
