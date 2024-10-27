import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def openDirectoryDialog(pathEntry, exPath=None):
    # Open the QFileDialog to select a directory
    if exPath == None:
        dirPath = QFileDialog.getExistingDirectory(None, 'Select Directory')
    else:
        dirPath = QFileDialog.getExistingDirectory(None, 'Select Directory', exPath)

    if dirPath:
        # Set the directory path in the line edit
        pathEntry.setText(dirPath)
    return

def enableOptionButtons(pathEntry, buttonEnter, buttonCam, buttonGauss,dirLabel):
    # Check if the directory exists
    dir_path = pathEntry.text()
    if dir_path and os.path.isdir(dir_path):
        buttonEnter.setEnabled(False)
        buttonCam.setEnabled(True)
        buttonGauss.setEnabled(True)
        dirLabel.setText(f'Selected Directory: {dir_path}')
        dirPath = dir_path
    else:
        buttonEnter.setEnabled(True)
        buttonCam.setEnabled(False)
        buttonGauss.setEnabled(False)
        dirLabel.setText('No directory selected')
        dirPath = None
    return dirPath
 
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