import os

import logging
from utils.files.file_writer import create_folder_if_not_exists
from utils.parameters import PATHS
from utils.reporting import Reporting
import re, time

months = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre",
          "Decembre"]

possible_pattern = [
    # Annee#mois#jour#serie
    "[January|February|March|April|May|June|July|August|September|October|November|December]*_[0-9]{2}__[0-9]*",
    # mois#Annee#jour#serie
    "([0-9]{4})([0-9]{2})([0-9]{2})[-_]([0-9]*)",
    # annee mois jour heure minutes secondes
    "([0-9]{2})([0-9]{2})([0-9]{2})[-_]([0-9]*)",
    # annee mois jour heure minutes secondes
    "([0-9]{4})[-_]([0-9]{2})[-_]([0-9]{2})[\-\s]([0-9]{2})[h\:\-\s\.]([0-9]{2})[m\:\-\s\.]([0-9]{2})",
    "([0-9]{2})[-_]([0-9]{2})[-_]([0-9]{2})[\-\s]([0-9]{2})[h\:\-\s\.]([0-9]{2})[m\:\-\s\.]([0-9]{2})",
]


def extract_datetime_from_exif(file_exif):
    """
    try to find the dateTime inside the exif metadata
    :param file_exif:
    :return: a string composed of the date if found, an empty string if not
    """
    new_filename = file_exif.get("EXIF DateTimeOriginal")
    new_filename = str(new_filename).replace(" ", "_")
    # If DataTimeOriginal doesn't contains data we try another exif meta data
    if new_filename == "    " or new_filename is None or new_filename == "None":
        new_filename = file_exif.get("Image DateTime")
        new_filename = str(new_filename).replace(" ", "_")
    if new_filename == "" or new_filename is None or str(new_filename) == '':
        return ""
    else:
        Reporting.date_by_exif += 1
        return new_filename


def detect_file_date(file_path):
    """
    if the exif doesn't contains the date of creation, this method try to detect the date of the file based on the name
    if the filename doesn't match any pattern it use the system date of creation
    :param directory: directory of the file
    :param filename: the current name of the file
    :param root_folder: the directory where the file will end up
    :return: the final name of the file and the new directory
    """
    dest_directory = ""
    for pattern in possible_pattern:
        matches = re.match(pattern, file_path)
        if (matches != None):
            Logger.getLogger().info(matches.groups())

    # Last chance : get filesystem creation date
    match = time.gmtime(os.path.getmtime(file_path))
    final_name = repr(match[0]) + ":" + repr(match[1]) + ":" + repr(match[2]) + "_" + repr(
        match[3]) + ":" + repr(match[4]) + ":" + repr(match[5])
    return final_name, dest_directory

