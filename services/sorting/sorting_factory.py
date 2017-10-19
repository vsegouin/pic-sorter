# coding=utf-8

from services.sorting import image_sorting
from utils.constants import MIMES_TYPES


def manage_file(file_path, mimes_type):
    print(file_path)
    if mimes_type == MIMES_TYPES.IMAGE:
        return image_sorting.sort_image(file_path)
    else:
        manage_non_image(file_path)


# @todo:REFACTOR
def manage_duplicate_file(file_path):
    print(file_path)


#    file_writer.copy_directory_structure(PATHS.root_path)


# @todo:REFACTOR
def manage_non_image(file_path):
    print(file_path)
