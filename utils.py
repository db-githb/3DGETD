import os
import datetime as dt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QLineEdit

subDirLst = ["models", "data"]

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
    parent.savedFlag = False
    parent.pathRoot = inPath.text()
    parent.pathEntry = QLineEdit()
    parent.pathEntry.setText(parent.pathRoot)

    # Generate full paths for the subdirectories depending on which window is being generated
    if name == "Experiment":
        full_paths = {subDir: os.path.join(parent.pathRoot, subDir) for subDir in subDirLst}
    else:
        full_paths = {subDirLst[1]: os.path.join(parent.pathRoot, subDirLst[1])}

    # Check which paths do not exist - don't worry about models subdir when creating cameras
    missing_dirs = {subDir: path for subDir, path in full_paths.items() if not os.path.isdir(path)}

    if missing_dirs:
        # Create a message listing all missing directories
        missing_str = ", ".join(missing_dirs.keys())
        missing_list = ''.join(f'<li>{item}</li>' for item in missing_str.split(','))
        reply = QMessageBox.question(parent,
                                    'Create New Project',
                                    f'Create new project in:<br>'
                                    f'<br>{parent.pathRoot}<br><br>'
                                    f'The following subdirectories will be created:'
                                    f'<div style="text-align: center;"><ul style="text-align: left;">{missing_list}</ul></div>'
                                    f'Do you want to continue?</div>',
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.Yes
                                )

        # Create Directories
        if reply == QMessageBox.Yes:
            for dirs, path in missing_dirs.items():
                try:
                    os.makedirs(path, exist_ok=True)
                except Exception as e:
                    QMessageBox.warning(
                        parent,
                        'Invalid Directory',
                        f'Could not create the "{dirs}" directory: {e}'
                    )
        else:
            parent.showWindow = False
            return

    # set pathEntry to models to ensure that browse opens to correct location
    if parent.name == "Experiment":
        parent.pathEntry.setText(os.path.join(parent.pathRoot, "models"))
        parent.pathRoot = parent.pathEntry.text()
    else:
        parent.pathEntry.setText(os.path.join(parent.pathRoot, "data"))
        parent.pathRoot = parent.pathEntry.text()

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
    if name == "Cameras":
        parent.buttonBrowse.clicked.connect(lambda: setImgSize(parent))
    parent.pathLayout.addWidget(parent.buttonBrowse)

    # Create an Enter button for the user to confirm the directory
    parent.buttonEnter = QPushButton(f"Create {name} Directory", parent)
    parent.buttonEnter.setEnabled(False)
    parent.buttonEnter.clicked.connect(lambda: checkDirectoryValidity(parent))
    parent.layout.addWidget(parent.buttonEnter)

    # Display full directory path for experiment
    parent.labelPath = QLabel(f'Selected Directory: {parent.pathEntry.text()}')
    parent.layout.addWidget(parent.labelPath)

    parent.showWindow = True # set flag during initialization so that values persist after window is closed

def completePath(parent, event=None):
    dirPath = parent.pathEntry.text()
    if hasattr(parent, "pathDir"): # non-main_windows have pathDir attributes
            # add user input to root project path
            dirPath = os.path.join(parent.pathRoot, parent.pathDir.text())
            parent.pathEntry.setText(dirPath) # display folder name
            parent.labelPath.setText(f'Selected Directory: {dirPath}') # full display project path
            
    return dirPath

def setImgSize(parent):
    pathData = parent.pathEntry.text()
    cameras_txt_filepath = os.path.join(pathData, "cameras.txt")
    if os.path.exists(cameras_txt_filepath):
        with open(cameras_txt_filepath, "r") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                line = line.strip()
                if len(line) > 0 and line[:-1] == "# Number of cameras: ":
                    parent.numExistingCams = int(line[-1])
                    parent.num_cameras_entry.setText(str(parent.numExistingCams))
                elif len(line) > 0 and line[0] != "#":
                    elems = line.split()
                    parent.imageWidth.setText(str(elems[2:3][0]))
                    parent.imageHeight.setText(str(elems[3:4][0]))
                    break # all images should be the same size so only need the one value

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

    status = parent.statusBP if hasattr(parent, "pathDir") else True
    if hasattr(parent, "statusCam"):
        status = status and parent.statusCam

    basename = os.path.basename(dirPath)
    if dirPath and os.path.isdir(dirPath) and basename != "" and basename != ".":
        if hasattr(parent, "buttonEnter"): parent.buttonEnter.setEnabled(False)
        if hasattr(parent, "buttonCam"): parent.buttonCam.setEnabled(status)
        if hasattr(parent, "buttonGauss"): parent.buttonGauss.setEnabled(status)
        if hasattr(parent, "buttonGenerate"): parent.buttonGenerate.setEnabled(status)
        if hasattr(parent, "buttonParams"): parent.buttonParams.setEnabled(True)
        if hasattr(parent, "labelPath"): parent.labelPath.setText(f'Selected Directory: {dirPath}')
    else:
        if hasattr(parent, "buttonEnter") and basename != "":
            parent.buttonEnter.setEnabled(True)
        else:
            parent.buttonEnter.setEnabled(False)   
        if hasattr(parent, "buttonCam"): parent.buttonCam.setEnabled(False)
        if hasattr(parent, "buttonGauss"): parent.buttonGauss.setEnabled(False)
        if hasattr(parent, "buttonGenerate"): parent.buttonGenerate.setEnabled(False)
        if hasattr(parent, "buttonParams"): parent.buttonParams.setEnabled(False)
        if hasattr(parent, "labelPath") and parent.__class__.__name__ == "MainWindow": 
            parent.labelPath.setText('No directory selected')
        # reset buttonParam status
        if hasattr(parent, "statusBP"): parent.statusBP = False

def checkDirectoryValidity(parent):
    # Check if the directory exists and ask the user if they want to create it if it doesn't
    dir_path = completePath(parent)
    if not dir_path or not os.path.isdir(dir_path):
        reply = QMessageBox.question(parent, 'Create Directory', f'The directory "{dir_path}" does not exist. Do you want to create it?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            try:
                os.makedirs(dir_path, exist_ok=True)
                toggleButtons(parent) # Update the state of the option buttons after creating the directory
            except Exception as e:
                QMessageBox.warning(parent, 'Invalid Directory', f'Could not create the directory: {e}')
                return
        else:
            return

def connectLineEdits(parent):
    for line_edit in parent.findChildren(QLineEdit):
        line_edit.textChanged.connect(lambda: removeTimeStamp(parent))

def savedTimeStamp(parent):
    #parent.labelSaved = QLabel(f"Saved: {dt.datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    #parent.labelSaved.setAlignment(Qt.AlignCenter)
    #parent.layout.addWidget(parent.labelSaved)
    parent.originalText = parent.buttonGenerate.text()
    parent.buttonGenerate.setText(f"Saved: {dt.datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    parent.savedFlag = True
    parent.buttonGenerate.setEnabled(False)

def removeTimeStamp(parent):
    if parent.savedFlag == True:
        #parent.layout.removeWidget(parent.labelSaved)
        #parent.labelSaved.deleteLater()
        parent.savedFlag = False
        parent.buttonGenerate.setText(parent.originalText)
        parent.buttonGenerate.setEnabled(True)