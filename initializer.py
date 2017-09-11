from utils.files.file_writer import create_folder_if_not_exists
from utils.parameters import PATHS


def initialize():
    create_folder_if_not_exists(PATHS.duplicate_folder)
    create_folder_if_not_exists(PATHS.processed_folder)
    file = open(PATHS.md5_database_path, "a", 1)
    file.close()
