import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QLineEdit

subDirDict = {"Experiment": "test_models", "Cameras": "data"}

class CustomLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = None  # This will be set to the main window instance later

    def setWindow(self, window):
        self.parent = window

    def keyPressEvent(self, event):
        # Call the parent class keyPressEvent to retain default behavior
        super().keyPressEvent(event)
        toggleButtons(self.parent, event)

def userInputLayout(parent, inPath):
    name = parent.name
    path = inPath.text()
    parent.pathEntry = QLineEdit()
    parent.pathEntry.setText(path)
    # Check if test_models directory exists, if not, create it
    if os.path.basename(os.path.normpath(path)) != subDirDict[name]:
        pathGG = os.path.join(path, subDirDict[name])
        parent.pathEntry.setText(pathGG)
        if not os.path.exists(pathGG):
          os.makedirs(pathGG)

    # Path selection
    parent.pathLayout = QHBoxLayout()
    parent.labelExp = QLabel(f"{name} Name: ")
    parent.pathDir = CustomLineEdit(parent)
    parent.pathDir.setWindow(parent)
    parent.pathDir.returnPressed.connect(lambda: checkDirectoryValidity(parent))
    parent.pathLayout.addWidget(parent.labelExp)
    parent.pathLayout.addWidget(parent.pathDir)
    parent.layout.addLayout(parent.pathLayout)

    # Create a button to open the directory dialogpath
    parent.buttonBrowse = QPushButton("Browse")
    parent.buttonBrowse.clicked.connect(lambda: openDirectoryDialog(parent))
    parent.pathLayout.addWidget(parent.buttonBrowse)

    # Create an Enter button for the user to confirm the directory
    parent.buttonEnter = QPushButton(f"Create {name} Directory", parent)
    parent.buttonEnter.setEnabled(False)
    parent.buttonEnter.clicked.connect(lambda: checkDirectoryValidity(parent))
    parent.layout.addWidget(parent.buttonEnter)

    # Display full directory path for experiment
    parent.labelPath = QLabel(f'Selected Directory: {parent.pathEntry.text()}')
    parent.layout.addWidget(parent.labelPath)

def completePath(parent, event=None):
    # pathEntry maintains root project path
    dirPath = parent.pathEntry.text()
    if hasattr(parent, "pathDir"): # non-main_windows have pathDir attributes
        # add subfolder to root project path
        if event != None and event.key() != Qt.Key_Backspace:
            # add user input to root project path
            dirPath = os.path.join(parent.pathEntry.text(), parent.pathDir.text())
            parent.pathEntry.setText(dirPath) # display folder name
            parent.labelPath.setText(f'Selected Directory: {dirPath}') # full display project path
        else:
            # ensure experiment folder is under test_models, otherwise when backspace is invoked it could create sub folders for every sub string when backspacing
            partsPath = dirPath.split(os.sep)
            index = partsPath.index(subDirDict[parent.name])
            dirPath = os.sep.join(partsPath[:index + 1])+"/"+parent.pathDir.text()
            parent.pathEntry.setText(dirPath)
            parent.labelPath.setText(f'Selected Directory: {dirPath}')
            
    return dirPath

def openDirectoryDialog(parent):
    # Open the QFileDialog to select a directory
    if hasattr(parent, "pathDir"):
        # Open to specfic path
        dirPath = QFileDialog.getExistingDirectory(None, 'Select Directory', parent.pathEntry.text())
        parent.pathDir.setText(os.path.basename(os.path.normpath(dirPath)))
        toggleButtons(parent)
    else:
        dirPath = QFileDialog.getExistingDirectory(None, 'Select Directory')

    # Set the directory path in the line edit
    parent.pathEntry.setText(dirPath)

def toggleButtons(parent, event=None):
        
    dirPath = completePath(parent, event)
    statusBG = parent.statusBP if hasattr(parent, "pathDir") else True

    if dirPath and os.path.isdir(dirPath) and os.path.basename(dirPath) != "":
        if hasattr(parent, "buttonEnter"): parent.buttonEnter.setEnabled(False)
        if hasattr(parent, "buttonCam"): parent.buttonCam.setEnabled(True)
        if hasattr(parent, "buttonGauss"): parent.buttonGauss.setEnabled(statusBG)
        if hasattr(parent, "buttonParams"): parent.buttonParams.setEnabled(True)
        if hasattr(parent, "labelPath"): parent.labelPath.setText(f'Selected Directory: {dirPath}')
    else:
        if hasattr(parent, "buttonEnter"): parent.buttonEnter.setEnabled(True)
        if hasattr(parent, "buttonCam"): parent.buttonCam.setEnabled(False)
        if hasattr(parent, "buttonGauss"): parent.buttonGauss.setEnabled(False)
        if hasattr(parent, "buttonParams"): parent.buttonParams.setEnabled(False)
        if hasattr(parent, "labelPath") and parent.__class__.__name__ == "MainWindow": 
            parent.labelPath.setText('No directory selected')
        # Clear base of path address as user types to prevent each letter being
        # added to pathEntry when program returns to completePath
        if hasattr(parent, "pathDir"): parent.pathEntry.setText(os.path.split(dirPath)[0])
        # reset buttonParam status
        if hasattr(parent, "statusBP"): parent.statusBP = False

 
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