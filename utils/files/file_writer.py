# coding=utf-8
import codecs
import logging
import os
import re
import sys

from utils.parameters import Parameters, PATHS
from utils.reporting import Reporting

logger = logging.getLogger(__name__)


def create_folder_if_not_exists(folder):
    from utils.reporting import Reporting
    """
    Check if the requested folder exists and create it if not
    :param folder:
    :return: the folder path created
    """
    if not os.path.exists(folder):
        if not Parameters.dry_run:
            os.makedirs(folder)
        Reporting.path_created.append(folder)
    return folder


def write_in_file(file, text):
    file = codecs.open(file, "a", "utf-8")
    file.write(text)
    file.write("\r\n")
    file.close()


def delete_files_list(file_list):
    logger.info(file_list)
    for duplicate_file in file_list:  # For each hash mode set
        logger.info('calling delete for ' + duplicate_file)
        delete_files_if_exists(duplicate_file)
        Reporting.file_deleted += 1


def delete_files_if_exists(file_path):
    logger.info(file_path)
    try:
        file_to_remove = ''.join(file_path.splitlines())
        if os.path.isfile(file_to_remove):
            os.remove(file_to_remove)
            logger.info("delete " + file_to_remove)
        else:
            logger.info("FILE DOESN'T EXISTS")
    except IndexError:
        logger.info("cannot delete " + repr(file_path))


def remove_line_from_file(file, line_number):
    f = open(file, "r")
    lines = f.readlines()
    f.close()
    f = open(file, "w")
    counter = 0
    for line in lines:
        counter = counter + 1
        if counter not in line_number:
            f.write(line)
    f.close()


def move_file(file_directory, filename, dest_directory, dest_filename):
    """
    This method clean the path created, check if a file already exists at this path and rename the file if needed
    It's possible that due to an error in the filename the programs can't move it
    :param file_directory: directory of the file to move
    :param filename: the name of the file to move
    :param dest_directory: the new directory of the file
    :param dest_filename: the new filename
    """
    from utils.reporting import Reporting
    dest_filename = re.sub('[<>:\"/|w?*]', '_', dest_filename)
    basename, extension = os.path.splitext(dest_filename)
    dst_file = os.path.join(dest_directory, dest_filename)
    # rename if necessary
    count = 0
    while os.path.exists(dst_file):
        count += 1
        dst_file = os.path.join(dest_directory, '%s-%d%s' % (basename, count, extension))
    # Reporting.log 'Renaming %s to %s' % (file, dst_file)
    try:
        if not Parameters.dry_run:
            os.rename(os.path.join(file_directory, filename), dst_file)
        Reporting.file_moved += 1
    except WindowsError or FileNotFoundError:
        Reporting.unmovable_file.append(os.path.join(file_directory, filename))
        logger.warning("CAN'T MOVE THIS FILE !!!!!")


def copy_directory_structure(directory_to_copy, directory_destination):
    """
    Copy the structure of a directory based on the root of the destination based on the root_path given in
    parameter
    >>> copy_directory_structure('C:/foo/bar/test/bar/foo','C:/foo/bar/process') #with C:/foo/bar as root_parameter
    'C:/foo/bar/process/test/bar/foo'
    :param directory_to_copy: the directory to copy (usually where the file is)
    :param directory_destination:
    :return:
    """
    sys.platform.system()
    new_directory = directory_to_copy.replace(PATHS.root_path, "")
    pattern = "^" + os.sep
    if Parameters.is_windows:
        pattern = "^" + os.sep + os.sep
    new_directory = re.sub(pattern, "", new_directory)
    new_directory = os.path.join(directory_destination, new_directory)
    try:
        create_folder_if_not_exists(new_directory)
    except FileNotFoundError:
        Reporting.unmovable_file.append(new_directory)
    return new_directory
