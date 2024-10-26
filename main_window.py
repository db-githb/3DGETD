import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QHBoxLayout, QMessageBox

from generate_gaussians import GaussianGenerator
from create_cameras import CreateCameras

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.cam_widget = None
        self.gauss_widget = None
        
        # Set up the main layout
        self.layout = QVBoxLayout()

        # Create a horizontal layout for the directory input field and button
        self.dirInputLayout = QHBoxLayout()

        # Create a line edit for the user to type the directory
        self.dirLineEdit = QLineEdit(self)
        self.dirLineEdit.returnPressed.connect(self.checkDirectoryValidity)
        self.dirLineEdit.textChanged.connect(self.enableOptionButtons)
        self.dirInputLayout.addWidget(self.dirLineEdit)

        # Create a button to open the directory dialog
        self.browseButton = QPushButton('Browse', self)
        self.browseButton.clicked.connect(self.openDirectoryDialog)
        self.dirInputLayout.addWidget(self.browseButton)

        # Add the directory input layout to the main layout
        self.layout.addLayout(self.dirInputLayout)

        # Create an Enter button for the user to confirm the directory
        self.buttonEnter = QPushButton('Enter', self)
        self.buttonEnter.clicked.connect(self.checkDirectoryValidity)
        self.layout.addWidget(self.buttonEnter)

        # Label to show the selected directory
        self.dirLabel = QLabel('No directory selected', self)
        self.layout.addWidget(self.dirLabel)

        # Option buttons (initially disabled)
        self.buttonCam = QPushButton('Create Cameras', self)
        self.buttonCam.setEnabled(False)
        self.buttonCam.clicked.connect(self.checkDirectoryValidity)
        self.buttonCam.clicked.connect(self.show_cam_window)
        self.layout.addWidget(self.buttonCam)

        self.buttonGauss = QPushButton('Generate Gaussians', self)
        self.buttonGauss.setEnabled(False)
        self.buttonGauss.clicked.connect(self.checkDirectoryValidity)
        self.buttonGauss.clicked.connect(self.show_gauss_window)
        self.layout.addWidget(self.buttonGauss)

        # Set the layout and window title
        self.setLayout(self.layout)
        self.setWindowTitle("3D Gaussian Generator")

    def openDirectoryDialog(self):
        # Open the QFileDialog to select a directory
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')

        if dir_path:
            # Set the directory path in the line edit
            self.dirLineEdit.setText(dir_path)

    def enableOptionButtons(self):
        # Check if the directory exists
        dir_path = self.dirLineEdit.text()
        if dir_path and os.path.isdir(dir_path):
            self.buttonCam.setEnabled(True)
            self.buttonGauss.setEnabled(True)
            self.dirLabel.setText(f'Selected Directory: {dir_path}')
        else:
            self.buttonCam.setEnabled(False)
            self.buttonGauss.setEnabled(False)
            #self.dirLabel.setText(f'Selected Directory: ')

    def checkDirectoryValidity(self):
        # Check if the directory exists and ask the user if they want to create it if it doesn't
        dir_path = self.dirLineEdit.text()
        if not dir_path or not os.path.isdir(dir_path):
            reply = QMessageBox.question(self, 'Create Directory', f'The directory "{dir_path}" does not exist. Do you want to create it?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    os.makedirs(dir_path, exist_ok=True)
                    self.enableOptionButtons() # Update the state of the option buttons after creating the directory
                except Exception as e:
                    QMessageBox.warning(self, 'Invalid Directory', f'Could not create the directory: {e}')
                    return
            else:
                return

    def show_cam_window(self):
        if self.cam_widget is None:
            self.cam_widget = CreateCameras()
        self.cam_widget.show()
    
    def show_gauss_window(self):
        if self.gauss_widget is None:
            self.gauss_widget = GaussianGenerator()   
        self.gauss_widget.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setMinimumSize(500, 100)
    window.show()
    sys.exit(app.exec_())
