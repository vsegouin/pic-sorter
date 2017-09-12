import logging

from utils.files.file_writer import create_folder_if_not_exists
from utils.parameters import PATHS, Parameters


def initialize():
    create_folder_if_not_exists(PATHS.duplicate_folder)
    create_folder_if_not_exists(PATHS.processed_folder)
    if Parameters.reset_database:
        file = open(PATHS.md5_database_path, "w", 1)
    else:
        file = open(PATHS.md5_database_path, "a", 1)
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
