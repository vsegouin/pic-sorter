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
from utils.files.file_writer import write_in_file
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
        write_in_file('dup', '----- Deduping : ' + PATHS.dedup_path[i] + ' ---------')
        write_in_file('unique_files', '----- Deduping : ' + PATHS.dedup_path[i] + ' ---------')
        for root, subdirs, files in file_crawler.crawl_folders(PATHS.dedup_path[i]):
            for file in files:
                file_path = os.path.join(root, file)
                exists, dup_file_path = check_duplication(file_path, True)
                if exists:
                    Reporting.duplicate_found += 1
                    write_in_file('dup', repr(file_path + ' = ' + dup_file_path).replace("\r\n", ""))
                    logger.info('file exists')
                else:
                    logger.info('file doesnt exists')
                    write_in_file('unique_files', dup_file_path)

                    # file_watcher.start_thread()

if Parameters.report:
    Reporting.do_reporting()
# while True:
#    time.sleep(1)
