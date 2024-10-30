import sys
import os
import torch
import json
import datetime as dt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QScrollArea, QGridLayout, QMessageBox
)

from utils import userInputLayout, openDirectoryDialog, checkDirectoryValidity

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

        # Main layout
        self.layout = QVBoxLayout()
        self.name = "Experiment"
        userInputLayout(self, inPath)
        
        # Number of Gaussians
        num_gaussians_layout = QHBoxLayout()
        num_gaussians_label = QLabel("Number of 3D Gaussians:")
        self.num_gaussians_entry = QLineEdit("2")  # Default to 2 Gaussians
        self.buttonParams = QPushButton("Create Parameter Fields")
        self.buttonParams.setEnabled(False)
        self.buttonParams.clicked.connect(self.create_input_fields)
        self.statusBP = False

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

    def create_input_fields(self):
        # set buttonParam status
        self.statusBP = True

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
            self.gaussian_layout.addWidget(QLabel("diffuse (base) color:"), row_offset + 1, 0)

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
            self.gaussian_layout.addWidget(QLabel("/255"), row_offset + 1, 4)
            self.features_entries.append([fe1, fe2, fe3])

            # means
            self.gaussian_layout.addWidget(QLabel("means:"), row_offset + 2, 0)
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
            self.gaussian_layout.addWidget(QLabel("quats:"), row_offset + 4, 0)
            qu1 = QLineEdit("0")
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

        self.adjustSize()
        self.buttonGauss.setEnabled(True)

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
                float(self.features_entries[i][0].text()), 
                float(self.features_entries[i][1].text()), 
                float(self.features_entries[i][2].text())
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
        self.data_path = "DUMMY VALUE" #"\n".join("- {dir}".format(dir=i) for i in range(path))

        yaml_content = f"""
        !!python/object:nerfstudio.engine.trainer.TrainerConfig
        _target: !!python/name:nerfstudio.engine.trainer.Trainer ''
        data: null
        experiment_name: {self.pathDir.text()}
        gradient_accumulation_steps: {{}}
        load_checkpoint: null
        load_config: null
        load_dir: null
        load_scheduler: true
        load_step: null
        log_gradients: false
        logging: !!python/object:nerfstudio.configs.base_config.LoggingConfig
          local_writer: !!python/object:nerfstudio.configs.base_config.LocalWriterConfig
            _target: !!python/name:nerfstudio.utils.writer.LocalWriter ''
            enable: true
            max_log_size: 10
            stats_to_track: !!python/tuple
            - !!python/object/apply:nerfstudio.utils.writer.EventName
              - Train Iter (time)
            - !!python/object/apply:nerfstudio.utils.writer.EventName
              - Train Rays / Sec
            - !!python/object/apply:nerfstudio.utils.writer.EventName
              - Test PSNR
            - !!python/object/apply:nerfstudio.utils.writer.EventName
              - Vis Rays / Sec
            - !!python/object/apply:nerfstudio.utils.writer.EventName
              - Test Rays / Sec
            - !!python/object/apply:nerfstudio.utils.writer.EventName
              - ETA (time)
          max_buffer_size: 20
          profiler: basic
          relative_log_dir: !!python/object/apply:pathlib.PosixPath []
          steps_per_log: 10
        machine: !!python/object:nerfstudio.configs.base_config.MachineConfig
          device_type: cuda
          dist_url: auto
          machine_rank: 0
          num_devices: 1
          num_machines: 1
          seed: 42
        max_num_iterations: 30000
        method_name: splatfacto
        mixed_precision: false
        optimizers:
          camera_opt:
            optimizer: !!python/object:nerfstudio.engine.optimizers.AdamOptimizerConfig
              _target: &id001 !!python/name:torch.optim.adam.Adam ''
              eps: 1.0e-15
              lr: 0.0001
              max_norm: null
              weight_decay: 0
            scheduler: !!python/object:nerfstudio.engine.schedulers.ExponentialDecaySchedulerConfig
              _target: &id002 !!python/name:nerfstudio.engine.schedulers.ExponentialDecayScheduler ''
              lr_final: 5.0e-07
              lr_pre_warmup: 0
              max_steps: 30000
              ramp: cosine
              warmup_steps: 1000
          features_dc:
            optimizer: !!python/object:nerfstudio.engine.optimizers.AdamOptimizerConfig
              _target: *id001
              eps: 1.0e-15
              lr: 0.0025
              max_norm: null
              weight_decay: 0
            scheduler: null
          features_rest:
            optimizer: !!python/object:nerfstudio.engine.optimizers.AdamOptimizerConfig
              _target: *id001
              eps: 1.0e-15
              lr: 0.000125
              max_norm: null
              weight_decay: 0
            scheduler: null
          means:
            optimizer: !!python/object:nerfstudio.engine.optimizers.AdamOptimizerConfig
              _target: *id001
              eps: 1.0e-15
              lr: 0.00016
              max_norm: null
              weight_decay: 0
            scheduler: !!python/object:nerfstudio.engine.schedulers.ExponentialDecaySchedulerConfig
              _target: *id002
              lr_final: 1.6e-06
              lr_pre_warmup: 1.0e-08
              max_steps: 30000
              ramp: cosine
              warmup_steps: 0
          opacities:
            optimizer: !!python/object:nerfstudio.engine.optimizers.AdamOptimizerConfig
              _target: *id001
              eps: 1.0e-15
              lr: 0.05
              max_norm: null
              weight_decay: 0
            scheduler: null
          quats:
            optimizer: !!python/object:nerfstudio.engine.optimizers.AdamOptimizerConfig
              _target: *id001
              eps: 1.0e-15
              lr: 0.001
              max_norm: null
              weight_decay: 0
            scheduler: null
          scales:
            optimizer: !!python/object:nerfstudio.engine.optimizers.AdamOptimizerConfig
              _target: *id001
              eps: 1.0e-15
              lr: 0.005
              max_norm: null
              weight_decay: 0
            scheduler: null
        output_dir: !!python/object/apply:pathlib.PosixPath
        - test_models
        pipeline: !!python/object:nerfstudio.pipelines.base_pipeline.VanillaPipelineConfig
          _target: !!python/name:nerfstudio.pipelines.base_pipeline.VanillaPipeline ''
          datamanager: !!python/object:nerfstudio.data.datamanagers.full_images_datamanager.FullImageDatamanagerConfig
            _target: !!python/name:nerfstudio.data.datamanagers.full_images_datamanager.FullImageDatamanager ''
            cache_images: cpu
            cache_images_type: uint8
            camera_res_scale_factor: 1.0
            data: null
            dataparser: !!python/object:nerfstudio.data.dataparsers.colmap_dataparser.ColmapDataParserConfig
              _target: !!python/name:nerfstudio.data.dataparsers.colmap_dataparser.ColmapDataParser ''
              assume_colmap_world_coordinate_convention: true
              auto_scale_poses: false
              center_method: none
              colmap_path: !!python/object/apply:pathlib.PosixPath
              - colmap
              - sparse
              - '0'
              data: !!python/object/apply:pathlib.PosixPath
              - data
              - {self.data_path}
              depth_unit_scale_factor: 0.001
              depths_path: null
              downscale_factor: 1
              downscale_rounding_mode: floor
              eval_interval: 8
              eval_mode: all
              images_path: !!python/object/apply:pathlib.PosixPath
              - images
              load_3D_points: true
              masks_path: null
              max_2D_matches_per_3D_point: 0
              orientation_method: none
              scale_factor: 1.0
              scene_scale: 1.0
              train_split_fraction: 0.9
            eval_image_indices: !!python/tuple
            - 0
            eval_num_images_to_sample_from: -1
            eval_num_times_to_repeat_images: -1
            images_on_gpu: false
            masks_on_gpu: false
            max_thread_workers: null
          model: !!python/object:nerfstudio.models.splatfacto.SplatfactoModelConfig
            _target: !!python/name:nerfstudio.models.splatfacto.SplatfactoModel ''
            background_color: random
            camera_optimizer: !!python/object:nerfstudio.cameras.camera_optimizers.CameraOptimizerConfig
              _target: !!python/name:nerfstudio.cameras.camera_optimizers.CameraOptimizer ''
              mode: 'off'
              optimizer: null
              rot_l2_penalty: 0.001
              scheduler: null
              trans_l2_penalty: 0.01
            collider_params:
              far_plane: 6.0
              near_plane: 2.0
            continue_cull_post_densification: true
            cull_alpha_thresh: 0.1
            cull_scale_thresh: 0.5
            cull_screen_size: 0.15
            densify_grad_thresh: 0.0008
            densify_size_thresh: 0.01
            enable_collider: true
            eval_num_rays_per_chunk: 4096
            loss_coefficients:
              rgb_loss_coarse: 1.0
              rgb_loss_fine: 1.0
            max_gauss_ratio: 10.0
            n_split_samples: 2
            num_downscales: 2
            num_random: 50000
            output_depth_during_training: false
            prompt: null
            random_init: false
            random_scale: 10.0
            rasterize_mode: classic
            refine_every: 100
            reset_alpha_every: 30
            resolution_schedule: 3000
            sh_degree: 3
            sh_degree_interval: 1000
            split_screen_size: 0.05
            ssim_lambda: 0.2
            stop_screen_size_at: 4000
            stop_split_at: 15000
            use_scale_regularization: false
            warmup_length: 500
        project_name: nerfstudio-project
        prompt: null
        relative_model_dir: !!python/object/apply:pathlib.PosixPath
        - nerfstudio_models
        save_only_latest_checkpoint: true
        steps_per_eval_all_images: 1000
        steps_per_eval_batch: 0
        steps_per_eval_image: 100
        steps_per_save: 2000
        timestamp: _unit_test
        use_grad_scaler: false
        viewer: !!python/object:nerfstudio.configs.base_config.ViewerConfig
          camera_frustum_scale: 0.1
          default_composite_depth: true
          image_format: jpeg
          jpeg_quality: 75
          make_share_url: false
          max_num_display_images: 512
          num_rays_per_chunk: 32768
          quit_on_train_completion: false
          relative_log_filename: viewer_log_filename.txt
          websocket_host: 0.0.0.0
          websocket_port: null
          websocket_port_default: 7007
        vis: viewer
        """

        # Modify the parameter by searching for the line containing it
        #for i, line in enumerate(yaml_content):
        #    if line.startswith(parameter_to_change + ':'):
        #        yaml_content[i] = f'{parameter_to_change}: {new_value}\n'
        #        break
        
        # Write the YAML string to a file - don't need to explicitly close the file, it is automatically closed when the block ends because of "with"
        with open(config_filepath, 'w') as file:
            file.write(yaml_content)

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
        os.makedirs(self.pathEntry.text() + "/nerfstudio_models/", exist_ok=True)

        # Check if the checkpoint file exists
        checkpoint_file = self.pathEntry.text() + "/nerfstudio_models/step-000029999.ckpt"
        if os.path.exists(checkpoint_file):
            # Load existing checkpoint
            checkpoint = torch.load(checkpoint_file)
        else:
            # Create a new checkpoint with default values
            checkpoint = {
                "step": 29999,
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
        torch.save(checkpoint, checkpoint_file) 
        print("End: SYSTEM TEST DATA " + str(dt.datetime.now().time()))


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GaussianGenerator()
    window.show()
    sys.exit(app.exec_())