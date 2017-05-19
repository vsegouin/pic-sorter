import logging
from logging import Logger

from Parameters import Parameters
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


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

    __metaclass__ = Singleton

    def reporting(self):
        pass

    @classmethod
    def increment_unauthorized_extension(cls, ext):
        try:
            cls.unauthorized_extension[ext] += 1
        except KeyError:
            cls.unauthorized_extension[ext] = 0
        cls.unauthorized_extension[ext] += 1
        pass

    @classmethod
    def doReporting(cls):
        print("\n\r\n\r===========================\n\r========Global infos=======\n\r===========================" +
              "\n\rTotal File found " + repr(cls.total_file) +
              "\n\rTotal File processed " + repr(cls.total_file_processed) +
              "\n\rTotal File Moved " + repr(cls.file_moved) +
              "\n\r\n\r===========================\n\r=======Type Detected=======\n\r===========================" +
              "\n\rImages found : " + repr(cls.image_found) +
              "\n\rVideos found : " + repr(cls.videos_found) +
              "\n\rOther found : " + repr(cls.other_found) +
              "\n\rDuplicate found : " + repr(cls.duplicate_found) +
              "\n\r\n\r===========================\n\r==Informations about image=\n\r===========================" +
              "\n\rImage with exif : " + repr(cls.image_with_exif) +
              "\n\rImage without exif : " + repr(cls.image_without_exif) +
              "\n\rDate found with exif : " + repr(cls.date_by_exif) +
              "\n\rDate found with filename : " + repr(cls.date_by_name) +
              "\n\rDate found with modification date : " + repr(cls.date_by_modified) +
              "\n\r\n\r===========================\n\r==========Errors===========\n\r===========================" +
              "\n\rErrors file : " + repr(cls.errors_files) +
              "\n\r\n\r===========================\n\r=Path of problematics file=\n\r===========================" +
              "\n\rUnmovable file : " + repr(cls.unmovable_file.__len__()) + "\n\r" +
              "\n\r".join(cls.unmovable_file) +
              "\n\r\n\r===========================\n\r=======Path created========\n\r===========================" +
              "\n\rPath Created : " + repr(list(set(cls.path_created)).__len__()) + "\n\r" +
              "\n\r".join(list(set(cls.path_created)))
              )

    @classmethod
    def log(cls, string):
        if Parameters.is_verbose:
            print(string)

    @classmethod
    def showProgress(cls,file,filePath):
        logging.info(repr(Reporting.total_file) + " / " + repr(Reporting.calculated_total_file)+" | "+file+" | "+repr(os.path.getsize(filePath) >> 20)+"Mo")
