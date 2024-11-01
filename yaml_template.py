def getYamlContent(pathDir, dataPath):
    yaml_content = f"""
        !!python/object:nerfstudio.engine.trainer.TrainerConfig
        _target: !!python/name:nerfstudio.engine.trainer.Trainer ''
        data: null
        experiment_name: {pathDir}
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
              - {dataPath}
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
        - {dataPath}
        save_only_latest_checkpoint: true
        steps_per_eval_all_images: 1000
        steps_per_eval_batch: 0
        steps_per_eval_image: 100
        steps_per_save: 2000
        timestamp: {dataPath}
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
    return yaml_content