# coding=utf-8
import logging
import os
import initializer
import utils.files.file_crawler as file_crawler
from services import mimes_detection
from services.detection import duplication_service
from services.sorting.sorting_factory import manage_file
from utils.hash import Hasher
from utils.parameters import Parameters, show_parameters, PATHS

Parameters.parse_args()
initializer.initialize()

logger = logging.getLogger(__name__)

show_parameters()
# file_crawler.count_total_find(PATHS.root_path)

for root, subdirs, files in file_crawler.crawl_folders(PATHS.root_path):
    for file in files:
        file_path = os.path.join(root, file)
        logger.debug('file : ' + file)
        # Hash MD5
        md5_hash = Hasher.hash_file('md5', file_path)
        logger.debug('md5 : '+md5_hash)
        sha1_hash = Hasher.hash_file('sha1', file_path)
        logger.debug('sha1 : '+sha1_hash)
        # File present in database
        md5_exists = duplication_service.is_file_already_present('md5', md5_hash)
        # Write hash if not exists
        if md5_exists:
            logger.debug("skip file")
            continue
        duplication_service.add_hash_to_database(md5_hash)
        # Hash SHA1

        # Get file type
        mime_types = mimes_detection.detect_image_file(file_path)
        manage_file(file_path, mime_types)

# file_watcher.start_thread()

# while True:
#    time.sleep(1)
