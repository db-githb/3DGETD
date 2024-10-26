import os
from random import randint
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QScrollArea, QGridLayout
)

# Default custom path
default_path = "/home/damian/projects/nerfstudio/data/_unit_test/" # "/your/default/path/"  # Replace this with your actual default path

class CreateCameras(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
    
    def __init__(self, dirPath=None):
        super().__init__()
        
        self.dir_path = dirPath
        self.setWindowTitle("Create Cameras")

        # Main layout
        layout = QVBoxLayout()

        # Path selection
        path_layout = QHBoxLayout()
        path_label = QLabel("Select Path:")
        self.path_entry = QLineEdit(default_path)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_path)

        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_entry)
        path_layout.addWidget(browse_button)
        layout.addLayout(path_layout)

        # Number of Cameras
        num_cameras_layout = QHBoxLayout()
        num_cameras_label = QLabel("Number of Cameras:")
        self.num_cameras_entry = QLineEdit("1")  # Default to 1 camera
        generate_button = QPushButton("Create Parameter Fields")
        generate_button.clicked.connect(self.create_input_fields)

        num_cameras_layout.addWidget(num_cameras_label)
        num_cameras_layout.addWidget(self.num_cameras_entry)
        num_cameras_layout.addWidget(generate_button)
        layout.addLayout(num_cameras_layout)

        # Scroll area for dynamically generated input fields
        min_width = 500
        min_height = 200
        self.scroll = QScrollArea()
        self.scroll.setMinimumSize(min_width,min_height)
        self.camera_frame = QWidget()
        self.camera_layout = QGridLayout(self.camera_frame)
        self.scroll.setWidget(self.camera_frame)
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)

        # Update button
        update_button = QPushButton("Create Cameras")
        update_button.clicked.connect(self.update_txt_files)
        layout.addWidget(update_button)

        # Set the main layout
        self.setLayout(layout)

        # Initialize storage for Camera input fields
        self.pos_entries = []
        self.quats_entries = []
    
    def browse_path(self):
        folder_selected = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder_selected:
            self.path_entry.setText(folder_selected + "/")

    def create_input_fields(self):
        # Clear previous entries if any
        for i in reversed(range(self.camera_layout.count())):
            widget_to_remove = self.camera_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()

        num_cameras = int(self.num_cameras_entry.text())

        self.pos_entries = []
        self.quats_entries = []

        for i in range(num_cameras):
            row_offset = i * 6  # Space out each Gaussian by 6 rows
            self.camera_layout.addWidget(QLabel(f"Camera {i+1}:"), row_offset, 0, 1, 8)

            # camera positions
            self.camera_layout.addWidget(QLabel("means:"), row_offset + 2, 0)
            p1 = QLineEdit("0")
            p2 = QLineEdit("0")
            p3 = QLineEdit("2.0")
            self.camera_layout.addWidget(p1, row_offset + 2, 1)
            self.camera_layout.addWidget(p2, row_offset + 2, 2)
            self.camera_layout.addWidget(p3, row_offset + 2, 3)
            self.pos_entries.append([p1, p2, p3])

            # camera quats
            self.camera_layout.addWidget(QLabel("quats:"), row_offset + 4, 0)
            q1 = QLineEdit("-0.707")
            q2 = QLineEdit("0")
            q3 = QLineEdit("0.707")
            q4 = QLineEdit("0")
            self.camera_layout.addWidget(q1, row_offset + 4, 1)
            self.camera_layout.addWidget(q2, row_offset + 4, 2)
            self.camera_layout.addWidget(q3, row_offset + 4, 3)
            self.camera_layout.addWidget(q4, row_offset + 4, 4)
            self.quats_entries.append([q1, q2, q3, q4])

    def update_txt_files(self):
        # Get user inputs
        ns_path = self.path_entry.text()
        num_cameras = int(self.num_cameras_entry.text())

        pos = []
        quats = []

        for i in range(num_cameras):
            # Get pos
            pos.append([
                float(self.pos_entries[i][0].text()), 
                float(self.pos_entries[i][1].text()), 
                float(self.pos_entries[i][2].text())
            ])

            # Get quats
            quats.append([
                float(self.quats_entries[i][0].text()), 
                float(self.quats_entries[i][1].text()), 
                float(self.quats_entries[i][2].text()), 
                float(self.quats_entries[i][3].text())
            ])

        # Check if file path exists, if it doesn't create it
        if not ns_path.endswith('/'):
            ns_path = ns_path + "/"
        os.makedirs(ns_path, exist_ok=True)

        # Create a cameras.txt file if it does't exist
        cameras_txt_filepath = ns_path + "cameras.txt"

        camera_line_template = "{id} PINHOLE 1000 1000 500 500 500 500"
        camera_lines = "\n".join(camera_line_template.format(id=i + 1) for i in range(num_cameras))

        cameras_content = f"""
# Camera list with one line of data per camera:
# CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]
# Number of cameras: {num_cameras}
{camera_lines}
        """

        with open(cameras_txt_filepath, 'w') as file:
            file.write(cameras_content)

        # Create a images.txt file if it does't exist
        images_txt_filepath = ns_path + "images.txt"

        image_lines_template = "{id}       {q1} {q2} {q3} {q4}       {p1} {p2} {p3}     {id} test.jpg"
        image_lines = "\n".join(image_lines_template.format(id=i + 1,
                                                            q1=quats[i][0],
                                                            q2=quats[i][1],
                                                            q3=quats[i][2],
                                                            q4=quats[i][3],
                                                            p1=pos[i][0],
                                                            p2=pos[i][1],
                                                            p3=pos[i][2],
                                                            ) for i in range(num_cameras))

        images_content = f"""
# Image list with two lines of data per image:
#   IMAGE_ID, QW, QX, QZ, QY, TX, TZ, TY, CAMERA_ID, NAME
#   POINTS2D[] as (X, Y, POINT3D_ID)
# Number of images: {num_cameras}, mean observations per image: 2537.3056478405315
{image_lines}
        """

        with open(images_txt_filepath, 'w') as file:
            file.write(images_content)