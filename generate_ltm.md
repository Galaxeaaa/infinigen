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
    python -m infinigen.datagen.manage_jobs --output_folder outputs/my_dataset --num_scenes 1 --pipeline_configs local_256GB.gin monocular.gin blender_gt.gin indoor_background_configs.gin --configs singleroom.gin --pipeline_overrides get_cmd.driver_script='infinigen_examples.generate_indoors' manage_datagen_jobs.num_concurrent=16 --overrides compose_indoors.restrict_single_supported_roomtype=True compose_indoors.hide_other_rooms_enabled=True compose_indoors.skirting_floor_enabled=False compose_indoors.skirting_ceiling_enabled=False
    ```
