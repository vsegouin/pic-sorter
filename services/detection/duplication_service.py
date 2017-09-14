# coding=utf-8
# Return true if Hash code is not blank and it's not present in database.txt

import logging

import sys

from utils.files.file_writer import write_in_file
from utils.hash import Hasher
from utils.parameters import PATHS, Parameters

logger = logging.getLogger(__name__)


def check_duplication(file_path):
    # Get hash files
    logger.debug('file : ' + file_path)
    is_present = True
    duplicate_file_path = None
    for hash_mode in Parameters.hash_modes:
        file_hash = Hasher.hash_file(hash_mode, file_path)
        hash_present, line_found, duplicate_file_path = is_file_already_present(hash_mode, file_hash)
        if not hash_present:
            write_in_file(PATHS.hash_databases.get(hash_mode), file_hash + '|' + file_path)
        is_present = is_present and hash_present


    # File present in database
    # Write hash if not exists
    if is_present:
        logger.info("file exists")
        write_in_file(PATHS.hash_databases.get('md5')+'toto',file_path+' = '+duplicate_file_path)
        return True
    else:
        return False


def is_file_already_present(type, hash):
    with open(PATHS.hash_databases.get(type), 'r', -1, sys.stdout.encoding) as myFile:
        for num, line in enumerate(myFile, 1):
            if hash in line:
                logger.debug(
                    type + ' ' + hash + ' found at line:' + repr(num) + ' duplicate file is : ' + line.split('|')[1])
                return True, num, line.split('|')[1]
    return False, None, None


'''
    f = open(PATHS.hash_databases.get(type))
    contents = f.read()
    f.close()
    if hash == "" or contents.count(hash) > 0:
        print(contents.find(hash))
        print(contents.index(hash))
        exit()
        return True
    else:
        return False

    return True if hash == "" or contents.count(hash) > 0 else False
'''
