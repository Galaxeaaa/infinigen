import glob
import logging
import os
import shutil
import sys


def delete_crashed_folders(job_dir):
    for job_path in glob.glob(os.path.join(job_dir, "dataset-*")):
        if not os.path.exists(job_path):
            print(f"Directory {job_path} does not exist.")
            continue

        crashed_file = os.path.join(job_path, "crashed_seeds.txt")

        if os.path.exists(crashed_file):
            with open(crashed_file, "r") as file:
                crashed_seeds = file.readlines()

            for seed in crashed_seeds:
                seed = seed.strip()
                seed_folder = os.path.join(job_path, seed)
                if os.path.exists(seed_folder) and os.path.isdir(seed_folder):
                    shutil.rmtree(seed_folder)
                    print(f"Deleted folder: {seed_folder}")


def count_seeds(job_dir):
    crashed_seeds = 0
    finished_seeds = 0

    # for all subdirectories in job_dir
    dataset_folders = glob.glob(os.path.join(job_dir, "dataset-*"))
    print(f"{len(dataset_folders)} dataset folders found")
    for dataset_path in dataset_folders:
        print(f"Counting {dataset_path}")
        crashed_file = os.path.join(dataset_path, "crashed_seeds.txt")
        finished_file = os.path.join(dataset_path, "finished_seeds.txt")

        if os.path.exists(crashed_file):
            with open(crashed_file, "r") as file:
                crashed_seeds += len(file.readlines())

        if os.path.exists(finished_file):
            with open(finished_file, "r") as file:
                finished_seeds += len(file.readlines())

    return crashed_seeds, finished_seeds


def delete_past_datasets(job_dir):
    for job_path in glob.glob(os.path.join(job_dir, "my_dataset_job_*")):
        shutil.rmtree(job_path)


def move_blend_to_new_folder(job_dir):
    job_dir = job_dir.rstrip("/")
    new_folder = job_dir + "_blend"
    os.makedirs(new_folder, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        handlers=[
            logging.FileHandler(os.path.join(new_folder, "move_blend.log"), mode="w"),
            logging.StreamHandler(),
        ],
    )

    dataset_folders = glob.glob(os.path.join(job_dir, "dataset-*"))
    logging.info(f"{len(dataset_folders)} dataset folders found")
    logging.info(f"Moving blend files from {job_dir} to {new_folder}")

    n_finished = 0
    n_moved = 0
    n_not_exist = 0
    n_duplicated = 0
    for dataset_path in dataset_folders:
        logging.info("")
        logging.info(f"Moving finished scenes in {dataset_path}")
        finished_file = os.path.join(dataset_path, "finished_seeds.txt")

        if os.path.exists(finished_file):
            with open(finished_file, "r") as file:
                finished_seeds = file.readlines()

            for seed in finished_seeds:
                n_finished += 1
                seed = seed.strip()
                seed_folder = os.path.join(dataset_path, seed)
                if os.path.exists(seed_folder) and os.path.isdir(seed_folder):
                    # move to job_dir/../job_dir + "blend"
                    new_seed_folder = os.path.join(new_folder, seed)
                    if os.path.exists(new_seed_folder):
                        n_duplicated += 1
                        logging.info(f"Folder {new_seed_folder} already exists.")
                        continue
                    blend_file = os.path.join(seed_folder, "coarse", "scene.blend")
                    # if blender_file exists, move it to new_folder
                    if os.path.exists(blend_file):
                        os.makedirs(new_seed_folder, exist_ok=True)
                        shutil.move(
                            blend_file, os.path.join(new_seed_folder, "scene.blend")
                        )
                        logging.info(f"Moved {blend_file} to {new_seed_folder}")
                        n_moved += 1
                    else:
                        logging.info(f"File {blend_file} does not exist.")
                        n_not_exist += 1

    logging.info("")
    logging.info("Summary")
    logging.info("====================================")
    logging.info(f"Found {n_finished} finished blend files.")
    logging.info(f"Moved {n_moved} blend files.")
    logging.info(f"Skipped {n_not_exist} non-existent folders.")
    logging.info(f"Skipped {n_duplicated} duplicated folders.")
    logging.info(
        f"Test passed: {n_finished == n_moved + n_not_exist + n_duplicated} (n_finished = n_moved + n_not_exist + n_duplicated)"
    )


def move_back(job_dir):
    for job_path in glob.glob(os.path.join(job_dir, "dataset-*_blend")):
        # move job_path/seed/scene.blend to job_path - "_blend"/seed/scene.blend
        for seed_path in glob.glob(os.path.join(job_path, "*")):
            blend_file = os.path.join(seed_path, "scene.blend")
            new_folder = os.path.join(
                os.path.dirname(job_path),
                os.path.basename(job_path)[:-6],
                os.path.basename(seed_path),
            )
            shutil.move(blend_file, os.path.join(new_folder, "scene.blend"))


if __name__ == "__main__":
    job_directory = sys.argv[2]
    if sys.argv[1] == "count":
        crashed_seeds, finished_seeds = count_seeds(job_directory)
        print(f"Crashed seeds: {crashed_seeds}")
        print(f"Finished seeds: {finished_seeds}")
    elif sys.argv[1] == "move_blend":
        move_blend_to_new_folder(job_directory)
    elif sys.argv[1] == "delete_crashed":
        delete_crashed_folders(job_directory)
    elif sys.argv[1] == "delete_past":
        job_directory = "/pv-bing/infinigen/outputs"
        delete_past_datasets(job_directory)
    elif sys.argv[1] == "move_back":
        move_back(job_directory)
