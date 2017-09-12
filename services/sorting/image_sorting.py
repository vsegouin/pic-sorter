# coding=utf-8

import os
import re
import time
import platform

from PIL import Image

from services.images import exif_reader
from services.images.exif_reader import get_exif_data, get_lat_lon, read_exif
import logging
from utils.date_utils import extract_datetime_from_exif, detect_file_date, months
from utils.files.file_writer import create_folder_if_not_exists, move_file
from utils.parameters import Parameters, PATHS
from utils.reporting import Reporting

unauthorizedExtension = ['.ico', '.gif']


def sort_image(file_path):
    image = Image.open(file_path)  # load an image through PIL's Image objec
    efix = read_exif(file_path)
    exif_data = get_exif_data(image)
    lon,lat = (get_lat_lon(exif_data))
        # GET EXIF
    # GET GEOLOCALISATION

    # GET DATE DONE


# Image type Dessin
# Image Type Photo

def manage_image(directory, filename, file_exif):
    """
    Methods which manage the image, prepare the new name, check if it's an authorized extension and then
    move it
    :param directory: directory of the file
    :param filename: name of the file
    :param file_exif: extracted exif data of the file
    """
    basename, ext = os.path.splitext(filename)
    try:
        dest_name = extract_datetime_from_exif(file_exif)
    except AttributeError:
        dest_name = ""
    root_folder = "regular"
    if file_exif == {} or dest_name == "" or dest_name == 'None' or re.search(r'(\d{4}):(\d{2}):(\d{2})',
                                                                              dest_name) == 'None':
        root_folder = "emptyExif"
        if ext in unauthorizedExtension:
            root_folder = "unauthorized"
        dest_name, dest_directory = detect_file_date(directory, filename, root_folder)
    else:
        try:
            match = re.search(r'(\d{4}):(\d{2}):(\d{2})', dest_name).groups()
            root_folder = "regular"
            if ext in unauthorizedExtension:
                root_folder = "unauthorized"
            dest_directory = create_folder_if_not_exists(
                os.path.join(PATHS.processed_folder, root_folder, repr(match[0]).replace("\\", "").replace("'", ""),
                             months[int(match[1]) - 1]))
        except AttributeError:
            root_folder = "error"
            dest_directory = create_folder_if_not_exists(
                os.path.join(PATHS.processed_folder, root_folder, filename))

    move_file(directory, filename, dest_directory, (dest_name + ext).replace(":", "-"))


def copy_directory_structure(self, directory_to_copy, directory_destination):
    """
    Copy the structure of a directory based on the root of the destination based on the root_path given in
    parameter
    >>> copy_directory_structure('C:/foo/bar/test/bar/foo','C:/foo/bar/process') #with C:/foo/bar as root_parameter
    'C:/foo/bar/process/test/bar/foo'
    :param directory_to_copy: the directory to copy (usually where the file is)
    :param directory_destination:
    :return:
    """
    platform.system()
    new_directory = directory_to_copy.replace(self.root_path, "")
    pattern = "^" + os.sep
    if Parameters.is_windows:
        pattern = "^" + os.sep + os.sep
    new_directory = re.sub(pattern, "", new_directory)
    new_directory = os.path.join(directory_destination, new_directory)
    try:
        self.create_folder_if_not_exists(new_directory)
    except FileNotFoundError:
        Reporting.unmovable_file.append(new_directory)
    return new_directory
