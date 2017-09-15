import logging

from utils.constants import MODE
from utils.files.file_writer import create_folder_if_not_exists
from utils.parameters import PATHS, Parameters


def initialize():
    if Parameters.application_mode == MODE.SORTER:
        create_folder_if_not_exists(PATHS.duplicate_folder)
        create_folder_if_not_exists(PATHS.processed_folder)
    if Parameters.reset_database:
        mode = "w"
    else:
        mode = "a"

    for hash_mode in Parameters.hash_modes:
        init_file(PATHS.hash_databases.get(hash_mode), mode)

    init_file(PATHS.duplicate_file_path, mode)
    init_file(PATHS.unique_file_path, mode)
    init_logger()


def init_file(file_path, mode):
    file = open(file_path, mode, 1)
    file.close()


def init_logger():
    log_format = '%(asctime)s - %(name)s - %(message)s'
    log_level = logging.INFO
    if Parameters.is_verbose:
        log_level = logging.DEBUG
    logging.basicConfig(format=log_format, level=log_level)
    # Disable PIL logging
    logging.getLogger('PIL.PngImagePlugin').setLevel(logging.WARNING)
