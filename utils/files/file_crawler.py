# coding=utf-8
import os
import logging
from utils.parameters import Parameters
from utils.reporting import Reporting

skipping_folders = ['@eaDir', 'processed', 'duplicate']

logger = logging.getLogger(__name__)


def crawl_folders(root_path):
    for root, subdirs, files in os.walk(root_path):
        if any(forbidden_path in root for forbidden_path in skipping_folders):
            continue
        logger.debug('-- current directory = ' + root)
        yield [root, subdirs, files]


def crawl_processed_folder(root_path):
    for root, subdirs, files in os.walk(root_path):
        if not "processed" in root:
            continue
        yield [root, subdirs, files]


def count_processed_file():
    logger.total_file = 0
    logger.calculated_total_file = 0
    for root, subdirs, files in crawl_processed_folder():
        logger.calculated_total_file += files.__len__()


def count_total_find(root_path):
    Reporting.total_file = 0
    Reporting.calculated_total_file = 0
    for root, subdir, files in crawl_folders(root_path):
        Reporting.total_file += files.__len__()
