# coding=utf-8
import logging

from services.images.exif_reader import get_exif_location, read_exif, get_exif_dimensions
from utils import date_utils
from utils.parameters import Parameters

logger = logging.getLogger(__name__)
logger.setLevel(Parameters.log_level)

unauthorizedExtension = ['.ico', '.gif']


def sort_image(file_path):
    logger.info(file_path)
    # GET EXIF
    exif_data = read_exif(file_path)
    if not exif_data == {}:
        # GET GEOLOCALISATION
        lon, lat = get_exif_location(exif_data)
        height, width, total = get_exif_dimensions(exif_data)
        date = date_utils.get_best_date(file_path, exif_data)
        # GET LOCALITY THANKS TO GEOCODING

        # GUESS BEST DATE


def manage_image(directory, filename, file_exif):
    pass;
    """
    @TODO: To Refactor '!!!'
    Methods which manage the image, prepare the new name, check if it's an authorized extension and then
    move it
    :param directory: directory of the file
    :param filename: name of the file
    :param file_exif: extracted exif data of the file



    basename, ext = os.path.splitext(filename)
    try:
        dest_name = extract_datetime_from_exif(file_exif)
    except AttributeError:
        dest_name = ""
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
    """
