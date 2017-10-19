import logging
import os

from utils.parameters import PATHS

logger = logging.getLogger(__name__)


# Python2
class Reporting(object):
    # global data
    file_deleted = 0
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
        from utils.files.file_writer import write_in_file

        report = ("\r\n\r\n===========================\r\n========Global infos=======\r\n===========================" +
                  "\r\nTotal File found " + repr(Reporting.total_file) +
                  "\r\nTotal File processed " + repr(Reporting.total_file_processed) +
                  "\r\nTotal File Moved " + repr(Reporting.file_moved) +
                  "\r\nTotal Deleted Files " + repr(Reporting.file_deleted) +
                  "\r\n\r\n===========================\r\n=======Type Detected=======\r\n===========================" +
                  "\r\nImages found : " + repr(Reporting.image_found) +
                  "\r\nVideos found : " + repr(Reporting.videos_found) +
                  "\r\nOther found : " + repr(Reporting.other_found) +
                  "\r\nDuplicate found : " + repr(Reporting.duplicate_found) +
                  "\r\n\r\n===========================\r\n==Informations about image=\r\n===========================" +
                  "\r\nImage with exif : " + repr(Reporting.image_with_exif) +
                  "\r\nImage without exif : " + repr(Reporting.image_without_exif) +
                  "\r\nDate found with exif : " + repr(Reporting.date_by_exif) +
                  "\r\nDate found with filename : " + repr(Reporting.date_by_name) +
                  "\r\nDate found with modification date : " + repr(Reporting.date_by_modified) +
                  "\r\n\r\n===========================\r\n==========Errors===========\r\n===========================" +
                  "\r\nErrors file : " + repr(Reporting.errors_files) +
                  "\r\n\r\n===========================\r\n=Path of problematics file=\r\n===========================" +
                  "\r\nUnmovable file : " + repr(Reporting.unmovable_file.__len__()) + "\r\n" +
                  "\r\n".join(Reporting.unmovable_file) +
                  "\r\n\r\n===========================\r\n=======Path created========\r\n===========================" +
                  "\r\nPath Created : " + repr(list(set(Reporting.path_created)).__len__()) + "\r\n" +
                  "\r\n".join(list(set(Reporting.path_created))))
        logger.info(report)
        write_in_file(PATHS.report_file_path, report)
        logger.info('Report can be read at ' + os.path.join(PATHS.report_file_path))

    @staticmethod
    def show_progress(file, file_path):
        logging.info(
            repr(Reporting.total_file) + " / " + repr(Reporting.calculated_total_file) + " | " + file + " | " + repr(
                os.path.getsize(file_path) >> 20) + "Mo")
