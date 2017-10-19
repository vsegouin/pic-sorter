# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os

from utils.parameters import PATHS
from utils.reporting import Reporting

skipping_folders = ['@eaDir', 'processed', 'duplicate']

logger = logging.getLogger(__name__)

logger.info("file  crawler init")


def crawl_folders(root_path):
    for root, subdirs, files in os.walk(root_path, False):
        if any(forbidden_path in root for forbidden_path in skipping_folders):
            continue
        logger.debug('-- current directory = ' + root)
        files_list = [os.path.join(root, file) for file in files]
        yield [root, files_list]


def crawl_recursive_leaf(root_path):
    index = 0
    for root, subdirs, files in os.walk(root_path):
        if any(forbidden_path in root for forbidden_path in skipping_folders):
            continue
        logger.debug('-- current directory = ' + root)
        logger.info(subdirs)
        index += 1
        yield [root, [os.path.join(root, file) for file in files]]


def crawl_processed_folder():
    for root, files in os.walk(PATHS.root_path):
        if not "processed" in root:
            continue
        yield [root, files]


def count_processed_file():
    logger.total_file = 0
    logger.calculated_total_file = 0
    for root, files in crawl_processed_folder():
        logger.calculated_total_file += files.__len__()


def count_total_find(root_path):
    Reporting.total_file = 0
    Reporting.calculated_total_file = 0
    for root, subdir, files in crawl_folders(root_path):
        Reporting.total_file += files.__len__()
