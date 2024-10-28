import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def openDirectoryDialog(parent):
    # Open the QFileDialog to select a directory
    if hasattr(parent, "pathInit"):
        dirPath = QFileDialog.getExistingDirectory(None, 'Select Directory', parent.pathInit)
    else:
        dirPath = QFileDialog.getExistingDirectory(None, 'Select Directory')

    if dirPath:
        # Set the directory path in the line edit
        parent.pathEntry.setText(dirPath)
    return

def toggleButtons(parent):
    # Check if the directory exists
    dir_path = parent.pathEntry.text()
    if dir_path and os.path.isdir(dir_path):
        if hasattr(parent, "buttonEnter"): parent.buttonEnter.setEnabled(False)
        if hasattr(parent, "buttonCam"): parent.buttonCam.setEnabled(True)
        if hasattr(parent, "buttonGauss"): parent.buttonGauss.setEnabled(True)
        if hasattr(parent, "buttonParams"): parent.buttonParams.setEnabled(True)
        if hasattr(parent, "labelDir"): parent.labelDir.setText(f'Selected Directory: {dir_path}')
        parent.pathDir = dir_path
    else:
        if hasattr(parent, "buttonEnter"): parent.buttonEnter.setEnabled(True)
        if hasattr(parent, "buttonCam"): parent.buttonCam.setEnabled(False)
        if hasattr(parent, "buttonGauss"): parent.buttonGauss.setEnabled(False)
        if hasattr(parent, "buttonParams"): parent.buttonParams.setEnabled(False)
        if hasattr(parent, "labelDir"): parent.labelDir.setText('No directory selected')

 
def checkDirectoryValidity(parent):
    # Check if the directory exists and ask the user if they want to create it if it doesn't
    if hasattr(parent, "pathInit"):
        dir_path = os.path.join(parent.pathInit, parent.pathEntry.text())
        parent.pathEntry.setText(dir_path)
    else:
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