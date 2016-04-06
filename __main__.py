import errno
from exifread import IfdTag

from files.FileBrowser import FileBrowser
from files.FileSystemManager import FileSystemManager
from files.MD5Encoder import MD5Encoder
from image.ExifReader import ExifReader

import os
import sys
import imghdr

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


def manageRegularImage(directory, filename, exif):
    new_filename = exif.get("EXIF DateTimeOriginal")
    print(exif.get("DateTimeOriginal"))
    directory = construct_new_directory(directory, os.path.join(fsManager.processed_folder, "regular"))
    os.rename(file_path, os.path.join(directory, filename))


def manageEmptyExif(directory, filename):
    directory = construct_new_directory(directory, os.path.join(fsManager.processed_folder, "emptyExif"))
    os.rename(file_path, os.path.join(directory, filename))
    pass


def manageNonImage(directory, filename):
    if (exif_reader.is_video(os.path.join(directory, filename))):
        directory = construct_new_directory(directory, os.path.join(fsManager.processed_folder, "video"))
    else:
        directory = construct_new_directory(directory, os.path.join(fsManager.processed_folder, "nonImage"))
    os.rename(file_path, os.path.join(directory, filename))
    pass


def manageDuplicateFiles(directory, filename):
    if not exif_reader.is_image(os.path.join(directory, filename)):
        if (exif_reader.is_video(os.path.join(directory, filename))):
            directory = construct_new_directory(directory, os.path.join(fsManager.duplicate_folder, "video"))
        else:
            directory = construct_new_directory(directory, os.path.join(fsManager.duplicate_folder, "nonImage"))
    else:
        directory = construct_new_directory(directory, fsManager.duplicate_folder)
    os.rename(file_path, os.path.join(directory, filename))
    pass


for root, subdirs, files in browser.crawl_folders():
    for file in files:
        file_path = os.path.join(root, file)
        if (file_path == fsManager.database_path):
            continue
        print("-----------------")
        browser.total_file_number += 1  # increment total number of files
        # If true the file doesn't exists and can be processed
        if not manageMD5(file_path):
            print("file is duplicate skip")
            manageDuplicateFiles(root, file)
            continue
        browser.total_file_number_processed += 1
        exif = exif_reader.read_exif(file_path)
        if not exif_reader.is_image(file_path):
            print("file is not an image")
            manageNonImage(root, file)
            continue
        if exif == {}:
            print("can't read EXIF, there is no data")
            manageEmptyExif(root, file)
            continue
        manageRegularImage(root, file, exif)

print(repr(browser.total_file_number) + " files found")
print(repr(browser.total_file_number_processed) + " files processed")
