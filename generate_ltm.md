1. Pull infinigen docker image.
    ```
    docker pull galaxeaaa/infinigen:latest
    ```

2. Run the docker image using the provided script.
    ```
    make docker-run
    ```

3. Attach to the running container.
    ```
    docker exec -it infinigen bash
    ```

4. Install additional dependencies.
    ```
    sudo apt-get install -y libsm6 libxext6 libxrender-dev
    ```

5. Run generation script.
    ```
    conda activate infinigen

    # Single room
    python -m infinigen_examples.generate_indoors --seed 0 --task coarse --output_folder outputs/indoors/bathroom -g fast_solve.gin singleroom.gin -p compose_indoors.terrain_enabled=False compose_indoors.room_doors_enabled=True compose_indoors.room_windows_enabled=True compose_indoors.hide_other_rooms_enabled=True compose_indoors.skirting_floor_enabled=False compose_indoors.skirting_ceiling_enabled=False restrict_solving.restrict_parent_rooms=\[\"Bathroom\"\] 

    # Automatic generation
    python -m infinigen.datagen.manage_jobs --output_folder outputs/room-shape-test/dataset --num_scenes 1 --pipeline_configs local_256GB.gin coarse_only.gin --configs fast_solve.gin singleroom.gin --pipeline_overrides get_cmd.driver_script='infinigen_examples.generate_indoors' manage_datagen_jobs.num_concurrent=8 LocalScheduleHandler.use_gpu=False --overrides compose_indoors.restrict_single_supported_roomtype=True compose_indoors.hide_other_rooms_enabled=True compose_indoors.skirting_floor_enabled=False compose_indoors.skirting_ceiling_enabled=False compose_indoors.skirting_floor_chance=0.0 compose_indoors.skirting_ceiling_chance=0.0 compose_indoors.room_pillars_chance=0.0

    python -m infinigen.datagen.manage_jobs --output_folder outputs/room-shape-test/dataset --num_scenes 1 --pipeline_configs local_256GB.gin coarse_only.gin --configs fast_solve.gin singleroom.gin --pipeline_overrides get_cmd.driver_script='infinigen_examples.generate_indoors' manage_datagen_jobs.num_concurrent=8 LocalScheduleHandler.use_gpu=False --overrides compose_indoors.skirting_floor_enabled=False compose_indoors.skirting_ceiling_enabled=False compose_indoors.skirting_floor_chance=0.0 compose_indoors.skirting_ceiling_chance=0.0 compose_indoors.room_pillars_chance=0.0 restrict_solving.restrict_parent_rooms=\[\"LivingRoom\"\]

    # Single room (Living room) per floorplan
    # - Batch
    python -m infinigen.datagen.manage_jobs --output_folder outputs/room-shape-test/dataset --num_scenes 8 --pipeline_configs local_256GB.gin coarse_only.gin --configs fast_solve.gin singleroom.gin --pipeline_overrides get_cmd.driver_script='infinigen_examples.generate_indoors' manage_datagen_jobs.num_concurrent=8 LocalScheduleHandler.use_gpu=False --overrides compose_indoors.terrain_enabled=False compose_indoors.room_doors_enabled=True compose_indoors.room_windows_enabled=True compose_indoors.hide_other_rooms_enabled=True compose_indoors.skirting_floor_enabled=False compose_indoors.skirting_ceiling_enabled=False compose_indoors.room_pillars_chance=0.0 restrict_solving.restrict_parent_rooms=\[\"LivingRoom\"\] RoomConstants.fixed_contour=True RoomConstants.room_type=\[\"LivingRoom\"\] RoomConstants.fixed_contour=True FloorPlanSolver.iters_mult=0 RoomConstants.aspect_ratio_range=\[1.0, 1.0\] RoomConstants.global_params.wall_thickness=0.2 RoomConstants.global_params.wall_height=3.0 GraphMaker.evaluate=False GraphMaker.slackness=1.2
    ```
