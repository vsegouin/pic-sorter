# coding=utf-8
import logging
import os
import initializer
import utils.files.file_crawler as file_crawler
from services import mimes_detection
from services.detection import duplication_service
from services.detection.duplication_service import check_duplication
from services.sorting.sorting_factory import manage_file
from utils.constants import MODE
from utils.files.file_writer import write_in_file, remove_line_from_file, delete_files_if_exists
from utils.hash import Hasher
from utils.parameters import Parameters, show_parameters, PATHS
from utils.reporting import Reporting

Parameters.parse_args()
initializer.initialize()

logger = logging.getLogger(__name__)

show_parameters()

# file_crawler.count_total_find(PATHS.root_path)



if Parameters.application_mode == MODE.SORTER:
    for root, subdirs, files in file_crawler.crawl_folders(PATHS.root_path):
        for file in files:
            file_path = os.path.join(root, file)
            if check_duplication(file_path):
                continue

            # Get file type
            mime_types = mimes_detection.detect_image_file(file_path)
            manage_file(file_path, mime_types)

elif Parameters.application_mode == MODE.DEDUP:
    for root, subdirs, files in file_crawler.crawl_folders(PATHS.dedup_path[0]):
        for file in files:
            file_path = os.path.join(root, file)
            check_duplication(file_path)

    logger.info('First file iteration done')
    for i in range(1, len(PATHS.dedup_path)):
        write_in_file(PATHS.duplicate_file_path, '----- Deduping : ' + PATHS.dedup_path[i] + ' ---------')
        write_in_file(PATHS.unique_file_path, '----- Deduping : ' + PATHS.dedup_path[i] + ' ---------')
        for root, subdirs, files in file_crawler.crawl_folders(PATHS.dedup_path[i]):
            for file in files:
                file_path = os.path.join(root, file)
                exists, hash_set, line_found_set, duplicate_file_path_set = check_duplication(file_path, False)
                if exists:
                    Reporting.duplicate_found += 1
                    for hash_mode in duplicate_file_path_set:
                        for dup_file_path in duplicate_file_path_set.get(hash_mode):
                            if Parameters.can_remove:
                                delete_files_if_exists(duplicate_file_path_set.get(hash_mode))
                                print(hash_set.get(hash_mode))
                                remove_line_from_file(PATHS.hash_databases.get(hash_mode), line_found_set.get(hash_mode))
                else:
                    write_in_file(PATHS.unique_file_path, file_path)

                    # file_watcher.start_thread()

if Parameters.report:
    Reporting.do_reporting()
# while True:
#    time.sleep(1)
