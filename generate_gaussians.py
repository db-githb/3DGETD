import os
import torch
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QScrollArea, QGridLayout, QMessageBox
)
from utils import userInputLayout, toggleButtons, savedTimeStamp
from yaml_template import getYamlContent

features_rest_1 = torch.tensor([[[ 3.7400e-02,  2.9200e-02,  3.2000e-03],
                              [ 1.0500e-02, -1.3500e-02, -1.2000e-02],
                              [-3.6000e-02, -3.1200e-02, -5.1600e-02],
                              [ 2.7300e-02,  2.7900e-02,  6.5700e-02],
                              [ 7.3000e-03, -5.9000e-03, -3.3400e-02],
                              [ 6.0000e-04, -1.0000e-03, -1.2900e-02],
                              [-7.6100e-02, -5.3600e-02, -3.7200e-02],
                              [-1.7000e-03,  9.0000e-04,  1.7900e-02],
                              [ 1.6630e-01,  1.3240e-01,  1.4840e-01],
                              [ 4.8400e-02,  3.5600e-02,  7.0500e-02],
                              [-6.5000e-03, -1.8500e-02, -5.2900e-02],
                              [ 2.4300e-02,  8.3000e-03, -3.1000e-03],
                              [-1.2010e-01, -8.5800e-02, -2.9300e-02],
                              [-6.7000e-03, -3.0000e-03, -7.1000e-03],
                              [ 3.8500e-02,  3.4700e-02, -1.2900e-02]]], device='cuda')

class GaussianGenerator(QWidget):
    def __init__(self):
        super().__init__()
    
    def __init__(self, inPath=None):
        super().__init__()

        self.name = "Experiment"
        self.statusBP = False # Flag to ensure that buttonGauss is only enabled when param values are loaded

        # Main layout
        self.layout = QVBoxLayout()
        userInputLayout(self, inPath)
        
        # Number of Gaussians
        num_gaussians_layout = QHBoxLayout()
        num_gaussians_label = QLabel("Number of 3D Gaussians:")
        self.num_gaussians_entry = QLineEdit("2")  # Default to 2 Gaussians
        self.buttonParams = QPushButton("Create Parameter Fields")
        self.buttonParams.setEnabled(False)
        self.buttonParams.clicked.connect(self.create_input_fields)

        num_gaussians_layout.addWidget(num_gaussians_label)
        num_gaussians_layout.addWidget(self.num_gaussians_entry)
        num_gaussians_layout.addWidget(self.buttonParams)
        self.layout.addLayout(num_gaussians_layout)

        # Scroll area for dynamically generated input fields
        min_width = 500
        min_height = 200
        self.scroll = QScrollArea()
        self.scroll.setMinimumSize(min_width,min_height)
        self.gaussian_frame = QWidget()
        self.gaussian_layout = QGridLayout(self.gaussian_frame)
        self.scroll.setWidget(self.gaussian_frame)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll)

        ############ CAMERA SELECTION ####################
        self.statusCam = False
        self.pathCamRoot =  os.path.join(inPath.text(), "data")
        os.makedirs(self.pathCamRoot, exist_ok=True)
        
        # Path selection
        self.pathCamLayout = QHBoxLayout()
        self.labelCamDir = QLabel("Select Cameras: ")
        self.pathCamDir = QLineEdit(self)
        self.pathCamDir.textChanged.connect(lambda: self.checkCamDirValidity())
        self.pathCamLayout.addWidget(self.labelCamDir)
        self.pathCamLayout.addWidget(self.pathCamDir)
        self.layout.addLayout(self.pathCamLayout)

        # Create a button to open the directory dialogpath
        self.buttonBrowseCams = QPushButton("Browse")
        self.buttonBrowseCams.clicked.connect(lambda: self.openCamDirectoryDialog())
        self.pathCamLayout.addWidget(self.buttonBrowseCams)
        #################################################

        # Update button
        self.buttonGauss = QPushButton("Generate Gaussians")
        self.buttonGauss.setEnabled(False)
        self.buttonGauss.clicked.connect(self.update_checkpoint)
        self.layout.addWidget(self.buttonGauss)

        # Set the layout and window title
        self.setLayout(self.layout)
        self.setWindowTitle("3D Gaussian Generator")

        # Initialize storage for Gaussian input fields
        self.features_entries = []
        self.means_entries = []
        self.opacity_entries = []
        self.quats_entries = []
        self.scales_entries = []

    def openCamDirectoryDialog(self):
      # Open the QFileDialog to data director
      dirPath = QFileDialog.getExistingDirectory(None, 'Select Directory', self.pathCamRoot)
      self.pathCamDir.setText(os.path.basename(os.path.normpath(dirPath)))
      self.checkCamDirValidity()
      # when you open directory dialogue but hit cancel without selecting anything, directory dialogue returns a "."
      # so need to directory validity to prevent buttonGauss being enabled for "." 
    
    def checkCamDirValidity(self):
        # Check if the directory exists and ask the user if they want to create it if it doesn't
        camDir = self.pathCamDir.text()
        fullCamPath = os.path.join(self.pathCamRoot, camDir)
        if os.path.isdir(fullCamPath) and camDir != "" and camDir != ".":
            self.statusCam = True
            toggleButtons(self)
        else:
            self.statusCam = False
            toggleButtons(self)

    def create_input_fields(self):
        # Clear previous entries if any
        for i in reversed(range(self.gaussian_layout.count())):
            widget_to_remove = self.gaussian_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()

        num_gaussians = int(self.num_gaussians_entry.text())

        self.features_entries = []
        self.means_entries = []
        self.opacity_entries = []
        self.quats_entries = []
        self.scales_entries = []

        for i in range(num_gaussians):
            row_offset = i * 6  # Space out each Gaussian by 6 rows
            self.gaussian_layout.addWidget(QLabel(f"<b>Gaussian {i+1}</b>:"), row_offset, 0, 1, 8)

            # features_dc
            labelFe = QLabel("color:")
            labelFe.setToolTip("Diffuse (base) color: R G B, range=(0,255)")
            self.gaussian_layout.addWidget(labelFe, row_offset + 1, 0)

            if i % 3 == 0:
                fe1 = QLineEdit("1")
                fe2 = QLineEdit("0")
                fe3 = QLineEdit("0")
            elif i % 3 == 1:
                fe1 = QLineEdit("0")
                fe2 = QLineEdit("1")
                fe3 = QLineEdit("0")
            elif i % 3 == 2:
                fe1 = QLineEdit("0")
                fe2 = QLineEdit("0")
                fe3 = QLineEdit("1")
            
            self.gaussian_layout.addWidget(fe1, row_offset + 1, 1)
            self.gaussian_layout.addWidget(fe2, row_offset + 1, 2)
            self.gaussian_layout.addWidget(fe3, row_offset + 1, 3)
            self.features_entries.append([fe1, fe2, fe3])

            # means
            labelMeans = QLabel("means:")
            labelMeans.setToolTip("Means: x y z")
            self.gaussian_layout.addWidget(labelMeans, row_offset + 2, 0)
            me1 = QLineEdit(str(i*2))
            me2 = QLineEdit("0")
            me3 = QLineEdit("0")
            self.gaussian_layout.addWidget(me1, row_offset + 2, 1)
            self.gaussian_layout.addWidget(me2, row_offset + 2, 2)
            self.gaussian_layout.addWidget(me3, row_offset + 2, 3)
            self.means_entries.append([me1, me2, me3])

            # opacities
            self.gaussian_layout.addWidget(QLabel("opacity:"), row_offset + 3, 0)
            op = QLineEdit("1")
            self.gaussian_layout.addWidget(op, row_offset + 3, 1)
            self.opacity_entries.append(op)

            # quats
            labelQuats = QLabel("quats:")
            labelQuats.setToolTip("Quaternions: w x y z\nNote: must be a unit length vector")
            self.gaussian_layout.addWidget(labelQuats, row_offset + 4, 0)
            qu1 = QLineEdit("1")
            qu2 = QLineEdit("0")
            qu3 = QLineEdit("0")
            qu4 = QLineEdit("0")
            self.gaussian_layout.addWidget(qu1, row_offset + 4, 1)
            self.gaussian_layout.addWidget(qu2, row_offset + 4, 2)
            self.gaussian_layout.addWidget(qu3, row_offset + 4, 3)
            self.gaussian_layout.addWidget(qu4, row_offset + 4, 4)
            self.quats_entries.append([qu1, qu2, qu3, qu4])

            # scales
            self.gaussian_layout.addWidget(QLabel("scales:"), row_offset + 5, 0)
            s1 = QLineEdit("0")
            s2 = QLineEdit("0")
            s3 = QLineEdit("0")
            self.gaussian_layout.addWidget(s1, row_offset + 5, 1)
            self.gaussian_layout.addWidget(s2, row_offset + 5, 2)
            self.gaussian_layout.addWidget(s3, row_offset + 5, 3)
            # self.gaussian_layout.addWidget(QLabel("Note: e^(scale)"), row_offset + 5, 4)
            self.scales_entries.append([s1, s2, s3])

        self.connectLineEdits()
        self.adjustSize()

        # Let enable buttonGauss now that default param values are loaded
        self.statusBP = True
        toggleButtons(self)

    def connectLineEdits(self):
        for line_edit in self.findChildren(QLineEdit):
            line_edit.textChanged.connect(self.removeTimeStamp)


    def update_checkpoint(self):
        # Get user inputs
        num_gaussians = int(self.num_gaussians_entry.text())

        features_dc = []
        means = []
        opacities = []
        quats = []
        scales = []

        for i in range(num_gaussians):
            # Get features_dc
            features_dc.append([
                int(self.features_entries[i][0].text()), 
                int(self.features_entries[i][1].text()), 
                int(self.features_entries[i][2].text())
            ])
            # Get means
            means.append([
                float(self.means_entries[i][0].text()), 
                float(self.means_entries[i][1].text()), 
                float(self.means_entries[i][2].text())
            ])
            # Get opacities
            opacities.append([float(self.opacity_entries[i].text())])
            # Get quats
            quats.append([
                float(self.quats_entries[i][0].text()), 
                float(self.quats_entries[i][1].text()), 
                float(self.quats_entries[i][2].text()), 
                float(self.quats_entries[i][3].text())
            ])
            # Get scales
            scales.append([
                float(self.scales_entries[i][0].text()), 
                float(self.scales_entries[i][1].text()), 
                float(self.scales_entries[i][2].text())
            ])

        # Create a config.yml file if it does't exist
        config_filepath = self.pathEntry.text() + "/config.yml"
        self.pathData = os.path.join(self.pathCamRoot, self.pathCamDir.text()) #"\n".join("- {dir}".format(dir=i) for i in range(path))

        yamlContent = getYamlContent(self.pathDir.text(), self.pathData, os.path.dirname(self.pathEntry.text()))
        
        # Write the YAML string to a file - don't need to explicitly close the file, it is automatically closed when the block ends because of "with"
        with open(config_filepath, 'w') as file:
            file.write(yamlContent)

        # Create JSON file if it doesn't exist
        json_filepath = self.pathEntry.text() + "/dataparser_transforms.json"
        if not os.path.exists(json_filepath):
            dataparser_transforms = {
                "transform": [ [1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, -1.0, 0.0, 0.0] ],
                "scale": 1.0
            }
            with open(json_filepath, 'w') as json_file:
                json.dump(dataparser_transforms, json_file, indent=4)  # indent=4 for pretty-printing

        # Check if parent directory for checkpoint exists, if it doesn't create it
        pathSplatfactoDir = os.path.join(self.pathEntry.text(), "splatfacto")
        os.makedirs(pathSplatfactoDir, exist_ok=True)

        # Check if the checkpoint file exists
        checkpoint_file =  os.path.join(pathSplatfactoDir, "step-000000000.ckpt")
        if os.path.exists(checkpoint_file):
            # Load existing checkpoint
            checkpoint = torch.load(checkpoint_file)
        else:
            # Create a new checkpoint with default values
            checkpoint = {
                "step": 0,
                "pipeline": {
                    "_model.gauss_params.features_dc": torch.zeros((num_gaussians, 3), device='cuda'),
                    "_model.gauss_params.features_rest": torch.zeros([num_gaussians,15,3], device="cuda"),
                    "_model.gauss_params.means": torch.zeros((num_gaussians, 3), device='cuda'),
                    "_model.gauss_params.opacities": torch.ones((num_gaussians, 1), device="cuda"),
                    "_model.gauss_params.quats": torch.zeros((num_gaussians, 4), device="cuda"),
                    "_model.gauss_params.scales": torch.zeros((num_gaussians, 3), device="cuda")
                }
            }
            print("Created a new checkpoint with default values.")

        # Update values in checkpoint
        checkpoint["pipeline"]["_model.gauss_params.features_dc"] = torch.tensor(features_dc, device='cuda')
        checkpoint["pipeline"]["_model.gauss_params.features_rest"] = torch.zeros([num_gaussians,15,3], device="cuda")
        checkpoint["pipeline"]["_model.gauss_params.means"] = torch.tensor(means, device='cuda')
        checkpoint["pipeline"]["_model.gauss_params.opacities"] = torch.tensor(opacities, device="cuda")
        checkpoint["pipeline"]["_model.gauss_params.quats"] = torch.tensor(quats, device="cuda")
        checkpoint["pipeline"]["_model.gauss_params.scales"] = torch.tensor(scales, device="cuda")

        # Save checkpoint
        try:
            torch.save(checkpoint, checkpoint_file)
            savedTimeStamp(self)
        except Exception as e:
              QMessageBox.critical(None, "Error", f"An error occurred: {e}")


        # points3D isn't actually used for rendering by NS BUT minimum 4 points are needed when loading the model of k-nearest neighbours
        points3D_txt_filepath = os.path.join(self.pathData, "points3D.txt")

        point_line_template = "{id} {x} {y} {z} {r} {g} {b} 0 0 0 0 0 0 0 0 0"
        id = range(num_gaussians)
        
        point_lines = "\n".join(point_line_template.format(
            id=i,
            x=m[0], y=m[1], z=m[2],
            r=c[0], g=c[1], b=c[2]) for i,m,c in zip(id, means, features_dc))
        
        num_points = num_gaussians
        if num_gaussians < 4:
            num_points = 4-num_gaussians
            point_lines_2 = "\n".join(point_line_template.format(
                id=i,
                x=i, y=i, z=i,
                r=i, g=i, b=i) for i in range(len(id), 4))
            point_lines += "\n"+point_lines_2
        
        cameras_content = f"""
# 3D point list with one line of data per point:
#   POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK[] as (IMAGE_ID, POINT2D_IDX)
# Number of points: {num_points}, mean track length: 3.3334
{point_lines}
        """

        with open(points3D_txt_filepath, 'w') as file:
            file.write(cameras_content)

    def removeTimeStamp(self):
        if self.savedFlag == True:
            self.layout.removeWidget(self.labelSaved)
            self.labelSaved.deleteLater()
            self.labelSaved = None
            self.savedFlag = False