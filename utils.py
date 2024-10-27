import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def openDirectoryDialog(self):
    # Open the QFileDialog to select a directory
    dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
    if dir_path:
        # Set the directory path in the line edit
        self.pathEntry.setText(dir_path)
    return

def enableOptionButtons(self):
    # Check if the directory exists
    dir_path = self.pathEntry.text()
    if dir_path and os.path.isdir(dir_path):
        self.buttonEnter.setEnabled(False)
        self.buttonCam.setEnabled(True)
        self.buttonGauss.setEnabled(True)
        self.dirLabel.setText(f'Selected Directory: {dir_path}')
        self.dirPath = dir_path
    else:
        self.buttonEnter.setEnabled(True)
        self.buttonCam.setEnabled(False)
        self.buttonGauss.setEnabled(False)
        self.dirLabel.setText('No directory selected')
        self.dirPath = None
    return
 
def checkDirectoryValidity(self):
    # Check if the directory exists and ask the user if they want to create it if it doesn't
    dir_path = self.pathEntry.text()
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