import logging

from utils.files.file_writer import create_folder_if_not_exists
from utils.parameters import PATHS, Parameters


def initialize():
    create_folder_if_not_exists(PATHS.duplicate_folder)
    create_folder_if_not_exists(PATHS.processed_folder)
    if Parameters.reset_database:
        mode = "w"
    else:
        mode = "a"

    for hash_mode in Parameters.hash_modes:
        print(hash_mode)
        file = open(PATHS.hash_databases.get(hash_mode), mode, 1)
        file.close()
    init_logger()


def init_logger():
    log_format = '%(asctime)s - %(name)s - %(message)s'
    log_level = logging.INFO
    if Parameters.is_verbose:
        log_level = logging.DEBUG
    logging.basicConfig(format=log_format, level=log_level)
    #Disable PIL logging
    logging.getLogger('PIL.PngImagePlugin').setLevel(logging.WARNING)
