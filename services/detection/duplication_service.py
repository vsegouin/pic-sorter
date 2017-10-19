# -*- coding: utf-8 -*-
# Return true if Hash code is not blank and it's not present in database.txt

import logging
import sys

from utils.files.file_writer import write_in_file
from utils.hash import Hasher
from utils.parameters import PATHS, Parameters

logger = logging.getLogger(__name__)


def check_duplication(file_path, add_hash=True):
    line_found_set = {}
    duplicate_file_path_set = set()
    hash_set = {}
    # For each hash modes set
    for hash_mode in Parameters.hash_modes:
        file_hash = Hasher.hash_file(hash_mode, file_path)  # Hash the file in the type asked
        # get data if the file is already present in the database
        hash_present, line_found_list, duplicate_file_path_list = is_file_already_present(hash_mode, file_hash)
        # If the parameter is set to add_hash, automatically add it to the database even if it's a duplicate or not
        if add_hash:
            write_in_file(PATHS.hash_databases.get(hash_mode), file_hash + '|' + file_path)  # Store it in the database
        if hash_present:  # if the file is already present in the database
            line_found_set.update({hash_mode: line_found_list})  # Add the line where the file has been found
            for i in duplicate_file_path_list:
                duplicate_file_path_set.add(i)  # Add all the files found in the database to delete them or trace them
            hash_set.update({hash_mode: file_hash})  # return the hash computed for the given type
    return len(line_found_set) == len(Parameters.hash_modes), hash_set, line_found_set, duplicate_file_path_set


def is_file_already_present(hash_modes, file_hash):
    num_list = []
    num_str_list = []
    # Open the file
    with open(PATHS.hash_databases.get(hash_modes), 'r', -1, sys.stdout.encoding) as myFile:
        for num, line in enumerate(myFile, 1):  # crawl all the lines
            if file_hash in line:
                num_list.append(num)  # Add the line where the occurence were found
                num_str_list.append(''.join(line.split('|')[1].splitlines()))  # Add the path of the duplicate
    return len(num_list) >= 1, num_list, num_str_list
