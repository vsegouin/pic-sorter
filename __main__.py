import logging
import time

from Parameters import Parameters
from Reporting import *
from files.FileBrowser import FileBrowser
from files.FileSystemManager import FileSystemManager
from files.MD5Encoder import MD5Encoder
from image.ExifReader import ExifReader

import os
import sys
import logging
logging.basicConfig(level=logging.INFO)
logging.debug("toto")
try:
    Parameters.root_path = sys.argv[1]
except IndexError:
    Reporting.log("PLEASE PROVIDE A PATH AS PARAMETER")
    exit(0)
try:
    if sys.argv[2] == 'true':
        Parameters.dry_run = True
    else:
        Parameters.dry_run = False
except IndexError:
    Parameters.dry_run = False

fsManager = FileSystemManager(Parameters.root_path)
browser = FileBrowser(fsManager.root_path)
md5_encryptor = MD5Encoder(fsManager.root_path)
exif_reader = ExifReader()

browser.count_total_find()
debut = time.time()

Reporting.log(repr(debut))
for root, subdirs, files in browser.crawl_folders():
    for file in files:
        # construct full image path
        file_path = os.path.join(root, file)
        # check if it's the database
        if file_path == fsManager.database_path:
            continue
        Reporting.log("-----------------")
        Reporting.total_file += 1  # increment total number of files
        Reporting.showProgress()
        # find the mime type
        file_type = exif_reader.detect_image_file(os.path.join(root, file))
        # check if a duplicate is already found
        try:
            if not md5_encryptor.process_md5(file_path):
                Reporting.log("file is duplicate skip")
                fsManager.manage_duplicate_file(root, file, file_type)
                continue
        except IOError:
            fsManager.manage_non_image(root, file, "error")
        # if it's not a duplicated file
        # we increment the number of unique file found
        Reporting.total_file_processed += 1
        # sort it in the folder if it's not an image
        if file_type == "video" or file_type == "other":
            fsManager.manage_non_image(root, file, file_type)
        # if it's an image
        elif file_type == "image":
            try:
                exif = exif_reader.read_exif(file_path)
                fsManager.manage_image(root, file, exif)
            except IOError:
                fsManager.manage_non_image(root, file, "error")

Reporting.doReporting()
if Parameters.dry_run:
    Reporting.log("This was a dry_run test, don't forget to delete the database.txt if it exists")
print("--- %s seconds ---" % (time.time() - debut))
