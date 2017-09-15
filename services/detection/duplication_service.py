# -*- coding: utf-8 -*-
# Return true if Hash code is not blank and it's not present in database.txt

import logging

import sys

from utils.files.file_writer import write_in_file
from utils.hash import Hasher
from utils.parameters import PATHS, Parameters

logger = logging.getLogger(__name__)


def check_duplication(file_path, add_hash=True):
    # Get hash files
    logger.debug('file : ' + file_path)
    # We check each hash
    line_found_set = {}
    duplicate_file_path_set = {}
    hash_set = {}
    for hash_mode in Parameters.hash_modes:
        file_hash = Hasher.hash_file(hash_mode, file_path)
        hash_present, line_found_list, duplicate_file_path_list = is_file_already_present(hash_mode, file_hash)
        # If file is found and auth to write in database
        if add_hash:
            write_in_file(PATHS.hash_databases.get(hash_mode), file_hash + '|' + file_path)
        if hash_present:
            line_found_set.update({hash_mode: line_found_list})
            duplicate_file_path_set.update({hash_mode: duplicate_file_path_list})
            hash_set.update({hash_mode: file_hash})

    return len(line_found_set) == len(Parameters.hash_modes), hash_set, line_found_set, duplicate_file_path_set


def is_file_already_present(type, hash):
    num_list = []
    num_str_list = []
    with open(PATHS.hash_databases.get(type), 'r', -1, sys.stdout.encoding) as myFile:
        for num, line in enumerate(myFile, 1):
            if hash in line:
                num_list.append(num)
                num_str_list.append(line.split('|')[1])
    return len(num_list) >= 1, num_list, num_str_list


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
