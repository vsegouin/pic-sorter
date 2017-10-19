import os

from utils.files import file_writer
from utils.parameters import PATHS
from utils.reporting import Reporting


def manage_duplicate_file(directory, filename, file_type):
    # @todo: REFACTOR !!!
    Reporting.duplicate_found += 1
    if file_type == "image":
        dest_directory = file_writer.copy_directory_structure(directory, PATHS.duplicate_folder)
    elif file_type == "video":
        dest_directory = file_writer.copy_directory_structure(directory, os.path.join(PATHS.duplicate_folder, "video"))
    else:
        dest_directory = file_writer.copy_directory_structure(directory, os.path.join(PATHS.duplicate_folder, "other"))

    file_writer.move_file(directory, filename, dest_directory, filename)
