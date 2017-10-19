import logging
import os
import re
import time

logger = logging.getLogger(__name__)

years_four = '(19[0-9]{2}|20[0-9]{2})'
months = '(0[1-9]|1[012])'
day = '(0[1-9]|1[0-9]|2[0-9]|3[01])'
years_two = '([0-9]{2})'
hours = '([01][0-9]|2[0-3])'
minutes = '([0-5][0-9])'
seconds = '([0-5][0-9])'
months_string = '(January|February|March|April|May|June|July|August|September|October|November|December)'
possible_pattern = [
    {"pattern": "{0}_{1}__{2}".format(years_four, months, day), "matches": ['year', 'month', 'day']},
    {"pattern": "{0}{1}{2}[-_]{3}{4}{5}*".format(years_four, months, day, hours, minutes, seconds),
     "matches": ["year", "month", "day", 'hours', 'minutes', 'seconds']},
    {"pattern": "{0}-{1}-{2}".format(years_four, months, day), "matches": ['year', 'month', 'day']},
    {"pattern": "{0}{1}{2}".format(years_four, months, day), "matches": ["year", "month", "day"]},
    {"pattern": "{0}{1}{2}[-_][0-9]*".format(years_two, months, day), "matches": ["year", "month", "day"]},
]


def extract_datetime_from_exif(file_exif):
    """
    try to find the dateTime inside the exif metadata
    :param file_exif:
    :return: a string composed of the date if found, an empty string if not
    """

    if file_exif is None or file_exif == {}:
        return None
    new_filename = file_exif.get("EXIF DateTimeOriginal")
    new_filename = str(new_filename).replace(" ", "_")
    # If DataTimeOriginal doesn't contains data we try another exif meta data
    if new_filename == "    " or new_filename is None or new_filename == "None":
        new_filename = file_exif.get("Image DateTime")
        new_filename = str(new_filename).replace(" ", "_")
        return new_filename
    if new_filename == "" or new_filename is None or str(new_filename) == '':
        return ""
    else:
        return new_filename


def detect_file_date_from_filename(file_path):
    """
    if the exif doesn't contains the date of creation, this method try to detect the date of the file based on the name
    if the filename doesn't match any pattern it use the system date of creation
    :param file_path: path of the file
    :return: the final name of the file and the new directory
    """
    for pattern in possible_pattern:
        matches = re.match(".*" + pattern.get('pattern') + ".*", file_path)
        if matches is not None:
            index = 0
            date = {}
            for element in matches.groups():
                date.update({pattern.get('matches')[index]: element})
                index += 1
            return date
    return None
    # Last chance : get filesystem creation date


def detect_file_date_from_os(file_path):
    match = time.gmtime(os.path.getmtime(file_path))
    date = {'year': repr(match[0]),
            'month': repr(match[1]).zfill(2),
            'day': repr(match[2]).zfill(2),
            'hour': repr(match[3]).zfill(2),
            'minutes': repr(match[4]).zfill(2),
            'seconds': repr(match[5]).zfill(2)
            }
    return date


def get_best_date(file_path, exif_data):
    date = extract_datetime_from_exif(exif_data)
    if date is None:
        date = detect_file_date_from_filename(file_path)
    if date is None:
        date = detect_file_date_from_os(file_path)
    return date
