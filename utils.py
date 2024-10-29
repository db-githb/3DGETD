import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def completePath(parent):
    if hasattr(parent, "pathDir"):
        # add subfolder to root project path
        dir_path = os.path.join(parent.pathEntry.text(), parent.pathDir.text(), )
        parent.pathEntry.setText(dir_path)
    else:
        # pathEntry maintains root project path
        dir_path = parent.pathEntry.text()
    return dir_path

def openDirectoryDialog(parent):
    # Open the QFileDialog to select a directory
    if hasattr(parent, "pathDir"):
        # Open to specfic path
        dirPath = QFileDialog.getExistingDirectory(None, 'Select Directory', parent.pathEntry.text())
        parent.pathDir.setText(os.path.basename(os.path.normpath(dirPath)))
    else:
        dirPath = QFileDialog.getExistingDirectory(None, 'Select Directory')

    # Set the directory path in the line edit
    parent.pathEntry.setText(dirPath)

def toggleButtons(parent):
    # Check if the directory exists
    dir_path = completePath(parent)
    if dir_path and os.path.isdir(dir_path):
        if hasattr(parent, "buttonEnter"): parent.buttonEnter.setEnabled(False)
        if hasattr(parent, "buttonCam"): parent.buttonCam.setEnabled(True)
        if hasattr(parent, "buttonGauss"): parent.buttonGauss.setEnabled(True)
        if hasattr(parent, "buttonParams"): parent.buttonParams.setEnabled(True)
        if hasattr(parent, "labelPath"): parent.labelPath.setText(f'Selected Directory: {dir_path}')
    else:
        if hasattr(parent, "buttonEnter"): parent.buttonEnter.setEnabled(True)
        if hasattr(parent, "buttonCam"): parent.buttonCam.setEnabled(False)
        if hasattr(parent, "buttonGauss"): parent.buttonGauss.setEnabled(False)
        if hasattr(parent, "buttonParams"): parent.buttonParams.setEnabled(False)
        if hasattr(parent, "labelPath") and parent.__class__.__name__ == "MainWindow": 
            parent.labelPath.setText('No directory selected')
        # Clear base of path address as user types to prevent each letter being
        # added to pathEntry when program returns to completePath
        if hasattr(parent, "pathDir"):  parent.pathEntry.setText(os.path.split(dir_path)[0])

 
def checkDirectoryValidity(parent):
    # Check if the directory exists and ask the user if they want to create it if it doesn't
    dir_path = completePath(parent)
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