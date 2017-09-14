# coding=utf-8
import os
import re

import sys

from utils.parameters import Parameters


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
    file = open(file, "a", 1)
    file.write(text)
    file.write("\r\n")
    file.close()


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
    dest_filename = re.sub('[<>:\"/\|\?*]', '_', dest_filename)
    basename, ext = os.path.splitext(dest_filename)
    dst_file = os.path.join(dest_directory, dest_filename)
    # rename if necessary
    count = 0
    while os.path.exists(dst_file):
        count += 1
        dst_file = os.path.join(dest_directory, '%s-%d%s' % (basename, count, ext))
    # Reporting.log 'Renaming %s to %s' % (file, dst_file)
    try:
        if not Parameters.dry_run:
            os.rename(os.path.join(file_directory, filename), dst_file)
        Reporting.file_moved += 1
    except WindowsError or FileNotFoundError:
        Reporting.unmovable_file.append(os.path.join(file_directory, filename))
        Reporting.log("CAN'T MOVE THIS FILE !!!!!")
