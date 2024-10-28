import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def openDirectoryDialog(parent):
    # Open the QFileDialog to select a directory
    if parent.pathExp == None:
        dirPath = QFileDialog.getExistingDirectory(None, 'Select Directory')
    else:
        dirPath = QFileDialog.getExistingDirectory(None, 'Select Directory', parent.pathExp)

    if dirPath:
        # Set the directory path in the line edit
        parent.pathEntry.setText(dirPath)
    return

def toggleButtons(parent):
    # Check if the directory exists
    dir_path = parent.pathEntry.text()
    if dir_path and os.path.isdir(dir_path):
        parent.buttonEnter.setEnabled(False) if parent.buttonEnter else None
        parent.buttonCam.setEnabled(True) if parent.buttonCam else None
        parent.buttonGauss.setEnabled(True) if parent.buttonGauss else None
        parent.labelDir.setText(f'Selected Directory: {dir_path}')
        parent.pathDir = dir_path
    else:
        parent.buttonEnter.setEnabled(True) if parent.buttonEnter else None
        parent.buttonCam.setEnabled(False) if parent.buttonCam else None
        parent.buttonGauss.setEnabled(False) if parent.buttonGauss else None
        parent.labelDir.setText('No directory selected')
        parent.labelDir = None
 
def checkDirectoryValidity(parent):
    # Check if the directory exists and ask the user if they want to create it if it doesn't
    dir_path = parent.pathEntry.text()
    if not dir_path or not os.path.isdir(dir_path):
        reply = QMessageBox.question(parent, 'Create Directory', f'The directory "{dir_path}" does not exist. Do you want to create it?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                os.makedirs(dir_path, exist_ok=True)
                toggleButtons(parent) # Update the state of the option buttons after creating the directory
            except Exception as e:
                QMessageBox.warning(parent, 'Invalid Directory', f'Could not create the directory: {e}')
                return
        else:
            return