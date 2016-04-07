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


def manageMD5(file_path):
    print(file_path)
    md5_encryptor.init_file(file_path)
    # if it's a duplicate or the database itself then there is no reason to continue
    if md5_encryptor.is_file_already_present():
        print(md5_encryptor.m_hashed_value + " already present")
        return False
    md5_encryptor.add_hash_in_database()
    print(md5_encryptor.m_hashed_value + " added")
    return True


def construct_new_directory(file_directory, new_folder):
    new_directory = file_directory.replace(fsManager.root_path, "")[1:]
    directory_structure = os.path.join(new_folder, new_directory)
    fsManager.create_folder_if_not_exists(directory_structure)
    return directory_structure


def extractDateTime(file_exif):
    new_filename = file_exif.get("EXIF DateTimeOriginal")
    new_filename = str(new_filename).replace(" ", "_")
    if new_filename == "" or new_filename == None or new_filename == "None":
        new_filename = file_exif.get("Image DateTime")
        new_filename = str(new_filename).replace(" ", "_")
    return "" if new_filename == "" or new_filename == None else new_filename



def manage_image(directory, filename, file_exif):
    if file_exif == {}:
        directory = construct_new_directory(directory, os.path.join(fsManager.processed_folder, "emptyExif"))
        os.rename(file_path, os.path.join(directory, filename))
    if file_exif != {}:
        new_filename = extractDateTime(file_exif)
        if new_filename == "":
            match = time.gmtime(os.path.getctime(os.path.join(directory, filename)))
            new_filename = repr(match[0]) + ":" + repr(match[1]) + ":" + repr(match[2]) + "_" + repr(
                    match[3]) + ":" + repr(match[4]) + ":" + repr(match[5])
        else:
            print(repr(new_filename))
            match = re.search(r'(\d{4}):(\d{2}):(\d{2})', new_filename).groups()
        directory = construct_new_directory(directory, os.path.join(fsManager.processed_folder, "regular",
                                                                    repr(match[0]).replace("\\", ""),
                                                                    repr(match[1]).replace("\\", ""),
                                                                    repr(match[2]).replace("\\", "")))
        os.rename(file_path, os.path.join(directory, new_filename))


def manage_non_image(directory, filename, file_type):
    if file_type == "video":
        directory = construct_new_directory(directory, os.path.join(fsManager.processed_folder, "video"))
    else:
        directory = construct_new_directory(directory, os.path.join(fsManager.processed_folder, "nonImage"))
    os.rename(file_path, os.path.join(directory, filename))


def manage_duplicate_file(directory, filename, file_type):
    if file_type == "image":
        directory = construct_new_directory(directory, fsManager.duplicate_folder)
    elif file_type == "video":
        directory = construct_new_directory(directory, os.path.join(fsManager.duplicate_folder, "videos"))
    else:
        directory = construct_new_directory(directory, os.path.join(fsManager.duplicate_folder, "otherd"))
    os.rename(file_path, os.path.join(directory, filename))


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
        if not manageMD5(file_path):
            print("file is duplicate skip")
            manage_duplicate_file(root, file, file_type)
            continue
        # if it's not a duplicated file
        # we increment the number of unique file found
        browser.total_file_number_processed += 1
        # sort it in the folder if it's not an image
        if file_type == "video" or file_type == "other":
            manage_non_image(root, file, file_type)
        # if it's an image
        elif file_type == "image":
            exif = exif_reader.read_exif(file_path)
            manage_image(root, file, exif)

print(repr(browser.total_file_number) + " files found")
print(repr(browser.total_file_number_processed) + " files processed")
