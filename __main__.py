# coding=utf-8
import logging

import initializer
import utils.files.file_crawler as file_crawler
from services import mimes_detection
from services.detection.duplication_service import check_duplication
from services.sorting.sorting_factory import manage_file, manage_duplicate_file
from utils.constants import MODE
from utils.files.file_writer import write_in_file, remove_line_from_file, delete_files_list
from utils.parameters import Parameters, show_parameters, PATHS
from utils.reporting import Reporting

Parameters.parse_args()
initializer.initialize()

logger = logging.getLogger(__name__)
logger.info(PATHS.root_path)
if Parameters.is_verbose:
    show_parameters()


def file_is_a_parameter(file_to_test):
    parameters_attr = [attr for attr in dir(PATHS) if
                       not callable(getattr(PATHS, attr))
                       and not attr.startswith("__")]
    for t in parameters_attr:
        if getattr(PATHS, t) is not None and file_to_test in getattr(PATHS, t):
            return True
    return False


if Parameters.application_mode == MODE.SORTER:
    for root, files in file_crawler.crawl_folders(PATHS.root_path):
        for file in files:
            if check_duplication(file)[0]:
                Reporting.duplicate_found += 1
                logger.info('file is duplicate')
                manage_duplicate_file(file)
                continue

            # Get file type
            mime_types = mimes_detection.detect_image_file(file)
            manage_file(file, mime_types)

elif Parameters.application_mode == MODE.DEDUP:

    # Crawl all the files of the first folder and store it in the differents databases
    for root, files in file_crawler.crawl_folders(PATHS.dedup_path[0]):
        for file_path in files:
            files.remove(file_path)
            # If the file is included in the list of the parameters, skip it
    for i in range(1, len(PATHS.dedup_path)):
        write_in_file(PATHS.duplicate_file_path, '-----  ' + PATHS.dedup_path[i] + ' ---------')
        write_in_file(PATHS.unique_file_path, '----- ' + PATHS.dedup_path[i] + ' ---------')
        for root, files in file_crawler.crawl_folders(PATHS.dedup_path[i]):
            for file_path in files:
                exists, hash_set, line_found_set, duplicate_file_path_set = check_duplication(file_path, False)
                # If file exists
                if exists:
                    if Parameters.can_remove:
                        delete_files_list(duplicate_file_path_set)
                    # Removes lines from databases as they no longer exist and shouldn't be used anymore
                    for hash_mode in line_found_set:
                        remove_line_from_file(PATHS.hash_databases.get(hash_mode), line_found_set.get(hash_mode))
                else:
                    write_in_file(PATHS.unique_file_path, file_path)

                    # file_watcher.start_thread()
                    # Crawls folder and delete folders if there is no more files
                    # TODO : Implements folder deletion
if Parameters.report:
    Reporting.do_reporting()
# while True:
#    time.sleep(1)
