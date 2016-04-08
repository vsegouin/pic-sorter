import errno

import re
from exifread import IfdTag

from files.FileBrowser import FileBrowser
from files.FileSystemManager import FileSystemManager
from files.MD5Encoder import MD5Encoder
from image.ExifReader import ExifReader
import time
import os
import sys

root_path = sys.argv[1]
fsManager = FileSystemManager(root_path)
browser = FileBrowser(fsManager.root_path)
md5_encryptor = MD5Encoder(fsManager.root_path)
exif_reader = ExifReader()

for root, subdirs, files in browser.crawl_folders():
    for file in files:
        # construct full image path
        file_path = os.path.join(root, file)
        # check if it's the database
        if file_path == fsManager.database_path:
            continue
        print("-----------------")
        browser.total_file_number += 1  # increment total number of files
        # find the mime type
        file_type = exif_reader.detect_image_file(os.path.join(root, file))
        # check if a duplicate is already found
        if not md5_encryptor.process_md5(file_path):
            print("file is duplicate skip")
            fsManager.manage_duplicate_file(root, file, file_type)
            continue
        # if it's not a duplicated file
        # we increment the number of unique file found
        browser.total_file_number_processed += 1
        # sort it in the folder if it's not an image
        if file_type == "video" or file_type == "other":
            fsManager.manage_non_image(root, file, file_type)
        # if it's an image
        elif file_type == "image":
            exif = exif_reader.read_exif(file_path)
            fsManager.manage_image(root, file, exif)

print(repr(browser.total_file_number) + " files found")
print(repr(browser.total_file_number_processed) + " files processed")
