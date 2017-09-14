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
            if check_duplication(file_path):
                continue

    for i in range(1, len(PATHS.dedup_path)):
        print(i)

        # file_watcher.start_thread()

# while True:
#    time.sleep(1)
