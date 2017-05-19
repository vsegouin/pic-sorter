# coding=utf-8
import os
import re
import time
import platform

from Parameters import Parameters
from Reporting import Reporting

months = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre",
          "Decembre"]
unauthorizedExtension = ['.ico', '.gif']


class FileSystemManager:
    root_path = ""
    database_path = ""
    duplicate_folder = ""
    processed_folder = ""

    def __init__(self, root_path):

        self.duplicate_file_path = os.path.join(root_path, "duplicate.txt")
        self.root_path = root_path
        self.database_path = os.path.join(root_path, "database.txt")
        self.duplicate_folder = os.path.join(root_path, "duplicate")
        self.processed_folder = os.path.join(root_path, "processed")
        self.init_folders()

    def init_folders(self):
        """
        Create the base folder (processed, duplicate folder)
        """
        self.create_folder_if_not_exists(self.duplicate_folder)
        self.create_folder_if_not_exists(self.processed_folder)

    def extract_datetime(self, file_exif):
        """
        try to find the dateTime inside the exif metadata
        :param file_exif:
        :return: a string composed of the date if found, an empty string if not
        """
        new_filename = file_exif.get("EXIF DateTimeOriginal")
        new_filename = str(new_filename).replace(" ", "_")
        # If DataTimeOriginal doesn't contains data we try another exif meta data
        if new_filename == "    " or new_filename is None or new_filename == "None":
            new_filename = file_exif.get("Image DateTime")
            new_filename = str(new_filename).replace(" ", "_")
        if new_filename == "" or new_filename is None or str(new_filename) == '':
            return ""
        else:
            Reporting.date_by_exif += 1
            return new_filename

    def create_folder_if_not_exists(self, folder):
        """
        Check if the requested folder exists and create it if not
        :param folder:
        :return: the folder path created
        """
        if not os.path.exists(folder):
            if not Parameters.dry_run:
                os.makedirs(folder)
            Reporting.path_created.append(folder)
        return folder

    def move_file(self, file_directory, filename, dest_directory, dest_filename):
        """
        This method clean the path created, check if a file already exists at this path and rename the file if needed
        It's possible that due to an error in the filename the programs can't move it
        :param file_directory: directory of the file to move
        :param filename: the name of the file to move
        :param dest_directory: the new directory of the file
        :param dest_filename: the new filename
        """
        dest_filename = re.sub('[<>:\"/\|\?*]', '_', dest_filename)
        basename, ext = os.path.splitext(dest_filename)
        dst_file = os.path.join(dest_directory, dest_filename)
        # rename if necessary
        count = 0
        while os.path.exists(dst_file):
            count += 1
            dst_file = os.path.join(dest_directory, '%s-%d%s' % (basename, count, ext))
        # Reporting.log 'Renaming %s to %s' % (file, dst_file)
        try:
            if not Parameters.dry_run:
                os.rename(os.path.join(file_directory, filename), dst_file)
            Reporting.file_moved += 1
        except WindowsError or FileNotFoundError:
            Reporting.unmovable_file.append(os.path.join(file_directory, filename))
            Reporting.log("CAN'T MOVE THIS FILE !!!!!")

    def manage_image(self, directory, filename, file_exif):

        """
        Methods which manage the image, prepare the new name, check if it's an authorized extension and then
        move it
        :param directory: directory of the file
        :param filename: name of the file
        :param file_exif: extracted exif data of the file
        """
        basename, ext = os.path.splitext(filename)
        try:
            dest_name = self.extract_datetime(file_exif)
        except AttributeError:
            dest_name = ""
        Reporting.image_found += 1
        root_folder="regular"
        if file_exif == {} or dest_name == "" or dest_name == 'None' or re.search(r'(\d{4}):(\d{2}):(\d{2})', dest_name) == 'None':
            root_folder = "emptyExif"
            if ext in unauthorizedExtension:
                root_folder = "unauthorized"
                Reporting.increment_unauthorized_extension(ext)
            else:
                Reporting.image_without_exif += 1
            dest_name, dest_directory = self.detect_file_date(directory, filename, root_folder)
        else:
            try:
                match = re.search(r'(\d{4}):(\d{2}):(\d{2})', dest_name).groups()
                root_folder = "regular"
                if ext in unauthorizedExtension:
                    root_folder = "unauthorized"
                    Reporting.increment_unauthorized_extension(ext)
                else:
                    Reporting.image_with_exif += 1
                dest_directory = self.create_folder_if_not_exists(os.path.join(self.processed_folder, root_folder, repr(match[0]).replace("\\", "").replace("'", ""), months[int(match[1]) - 1]))
            except AttributeError:
                Reporting.errors_files_details.append(os.path.join(directory,filename))
                Reporting.errors_files+=1
                root_folder="error"
                dest_directory = self.create_folder_if_not_exists(os.path.join(self.processed_folder, root_folder, filename))

        self.move_file(directory, filename, dest_directory, (dest_name + ext).replace(":", "-"))

    def manage_non_image(self, directory, filename, file_type):
        if file_type == "video":
            dest_directory = self.create_folder_if_not_exists(os.path.join(self.processed_folder, "video"))
            Reporting.videos_found += 1
        elif file_type == "error":
            dest_directory = self.create_folder_if_not_exists(os.path.join(self.processed_folder, "error"))
            Reporting.errors_files += 1
            Reporting.errors_files_details.append(os.path.join(directory, filename))
        else:
            dest_directory = self.copy_directory_structure(directory, os.path.join(self.processed_folder, "nonImage"))
            Reporting.other_found += 1
        try:
            self.move_file(directory, filename, dest_directory, filename)
        except:
            Reporting.unmovable_file.append(os.path.join(directory,filename))


    def manage_duplicate_file(self, directory, filename, file_type):
        Reporting.duplicate_found += 1
        if file_type == "image":
            dest_directory = self.copy_directory_structure(directory, self.duplicate_folder)
        elif file_type == "video":
            dest_directory = self.copy_directory_structure(directory, os.path.join(self.duplicate_folder, "video"))
        else:
            dest_directory = self.copy_directory_structure(directory, os.path.join(self.duplicate_folder, "other"))

        self.move_file(directory, filename, dest_directory, filename)

    def copy_directory_structure(self, directory_to_copy, directory_destination):
        """
        Copy the structure of a directory based on the root of the destination based on the root_path given in
        parameter
        >>> copy_directory_structure('C:/foo/bar/test/bar/foo','C:/foo/bar/process') #with C:/foo/bar as root_parameter
        'C:/foo/bar/process/test/bar/foo'
        :param directory_to_copy: the directory to copy (usually where the file is)
        :param directory_destination:
        :return:
        """
        platform.system()
        new_directory = directory_to_copy.replace(self.root_path, "")
        pattern = "^" + os.sep
        if Parameters.is_windows:
            pattern = "^" + os.sep + os.sep
        new_directory = re.sub(pattern, "", new_directory)
        new_directory = os.path.join(directory_destination, new_directory)
        try:
            self.create_folder_if_not_exists(new_directory)
        except FileNotFoundError:
            Reporting.unmovable_file.append(new_directory)
        return new_directory

    def detect_file_date(self, directory, filename, root_folder):
        """
        if the exif doesn't contains the date of creation, this method try to detect the date of the file based on the name
        if the filename doesn't match any pattern it use the system date of creation
        :param directory: directory of the file
        :param filename: the current name of the file
        :param root_folder: the directory where the file will end up
        :return: the final name of the file and the new directory
        """
        final_name = ""
        dest_directory = ""
        possible_pattern = [
            # Annee#mois#jour#serie
            "[January|February|March|April|May|June|July|August|September|October|November|December]*_[0-9]{2}__[0-9]*",
            # mois#Annee#jour#serie
            "([0-9]{4})([0-9]{2})([0-9]{2})[-_]([0-9]*)",
            # annee mois jour heure minutes secondes
            "([0-9]{2})([0-9]{2})([0-9]{2})[-_]([0-9]*)",
            # annee mois jour heure minutes secondes
            "([0-9]{4})[-_]([0-9]{2})[-_]([0-9]{2})[\-\s]([0-9]{2})[h\:\-\s\.]([0-9]{2})[m\:\-\s\.]([0-9]{2})",
            "([0-9]{2})[-_]([0-9]{2})[-_]([0-9]{2})[\-\s]([0-9]{2})[h\:\-\s\.]([0-9]{2})[m\:\-\s\.]([0-9]{2})",
        ]
        for pattern in possible_pattern:
            matches = re.match(pattern, final_name)
            if (matches != None):
                Reporting.log(matches.groups())
        # Last chance : get filesystem creation date
        if final_name == "":
            match = time.gmtime(os.path.getmtime(os.path.join(directory, filename)))
            final_name = repr(match[0]) + ":" + repr(match[1]) + ":" + repr(match[2]) + "_" + repr(
                match[3]) + ":" + repr(match[4]) + ":" + repr(match[5])
            dest_directory = self.create_folder_if_not_exists(
                os.path.join(self.processed_folder, root_folder, repr(match[0]), months[match[1] - 1], repr(match[2])))
            Reporting.date_by_modified += 1
        else:
            Reporting.date_by_name += 1
        return final_name, dest_directory
