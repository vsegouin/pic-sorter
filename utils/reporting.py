import logging
from utils.Logger import Logger
from utils.parameters import Parameters
import os

logger = Logger()


# Python2
class Reporting(object):
    # global data
    hashed = []
    calculated_total_file = 0
    total_file = 0  #
    total_file_processed = 0  #
    file_moved = 0
    # Type
    image_found = 0  #
    videos_found = 0  #
    duplicate_found = 0  #
    other_found = 0  #
    # Data on images
    image_with_exif = 0
    image_without_exif = 0
    date_by_exif = 0
    date_by_name = 0
    date_by_modified = 0

    # actions

    unauthorized_extension = {}
    errors_files = 0
    errors_files_details = []
    path_created = []

    unmovable_file = []

    def reporting(self):
        pass

    @staticmethod
    def increment_unauthorized_extension(ext):
        try:
            Reporting.unauthorized_extension[ext] += 1
        except KeyError:
            Reporting.unauthorized_extension[ext] = 0
        Reporting.unauthorized_extension[ext] += 1
        pass

    @staticmethod
    def do_reporting():
        logger.log("\n\r\n\r===========================\n\r========Global infos=======\n\r===========================" +
                   "\n\rTotal File found " + repr(Reporting.total_file) +
                   "\n\rTotal File processed " + repr(Reporting.total_file_processed) +
                   "\n\rTotal File Moved " + repr(Reporting.file_moved) +
                   "\n\r\n\r===========================\n\r=======Type Detected=======\n\r===========================" +
                   "\n\rImages found : " + repr(Reporting.image_found) +
                   "\n\rVideos found : " + repr(Reporting.videos_found) +
                   "\n\rOther found : " + repr(Reporting.other_found) +
                   "\n\rDuplicate found : " + repr(Reporting.duplicate_found) +
                   "\n\r\n\r===========================\n\r==Informations about image=\n\r===========================" +
                   "\n\rImage with exif : " + repr(Reporting.image_with_exif) +
                   "\n\rImage without exif : " + repr(Reporting.image_without_exif) +
                   "\n\rDate found with exif : " + repr(Reporting.date_by_exif) +
                   "\n\rDate found with filename : " + repr(Reporting.date_by_name) +
                   "\n\rDate found with modification date : " + repr(Reporting.date_by_modified) +
                   "\n\r\n\r===========================\n\r==========Errors===========\n\r===========================" +
                   "\n\rErrors file : " + repr(Reporting.errors_files) +
                   "\n\r\n\r===========================\n\r=Path of problematics file=\n\r===========================" +
                   "\n\rUnmovable file : " + repr(Reporting.unmovable_file.__len__()) + "\n\r" +
                   "\n\r".join(Reporting.unmovable_file) +
                   "\n\r\n\r===========================\n\r=======Path created========\n\r===========================" +
                   "\n\rPath Created : " + repr(list(set(Reporting.path_created)).__len__()) + "\n\r" +
                   "\n\r".join(list(set(Reporting.path_created)))
                   )

    @staticmethod
    def show_progress(file, file_path):
        logging.info(
            repr(Reporting.total_file) + " / " + repr(Reporting.calculated_total_file) + " | " + file + " | " + repr(
                os.path.getsize(file_path) >> 20) + "Mo")
