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
    python -m infinigen_examples.generate_indoors --seed 0 --task coarse --output_folder outputs/indoors/dining_room -g fast_solve.gin singleroom.gin -p compose_indoors.terrain_enabled=False compose_indoors.room_doors_enabled=True compose_indoors.room_windows_enabled=True compose_indoors.hide_other_rooms_enabled=True compose_indoors.skirting_floor_enabled=False compose_indoors.skirting_ceiling_enabled=False restrict_solving.restrict_parent_rooms=\[\"DiningRoom\"\] 
    ```