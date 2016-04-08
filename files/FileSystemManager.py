import os
import re
import time

from image.ExifReader import ExifReader

months = ["Janvier","Fevrier","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Decembre"]

class FileSystemManager:
    root_path = ""
    database_path = ""
    duplicate_folder = ""
    processed_folder = ""

    def __init__(self, root_path):
        self.root_path = root_path
        self.database_path = os.path.join(root_path, "database.txt")
        self.duplicate_folder = os.path.join(root_path, "duplicate")
        self.processed_folder = os.path.join(root_path, "processed")
        self.init_folders()

    def init_folders(self):
        if not os.path.exists(self.duplicate_folder):
            os.makedirs(self.duplicate_folder)
        if not os.path.exists(self.processed_folder):
            os.makedirs(self.processed_folder)

    def extract_datetime(self, file_exif):
        new_filename = file_exif.get("EXIF DateTimeOriginal")
        new_filename = str(new_filename).replace(" ", "_")
        if new_filename == "" or new_filename is None or new_filename == "None":
            new_filename = file_exif.get("Image DateTime")
            new_filename = str(new_filename).replace(" ", "_")
        return "" if new_filename == "" or new_filename is None else new_filename

    def create_folder_if_not_exists(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    def move_file(self, file_directory, filename, dest_directory, dest_filename):
        basename,ext = os.path.splitext(dest_filename)
        dst_file = os.path.join(dest_directory, dest_filename)
        # rename if necessary
        count = 0
        while os.path.exists(dst_file):
            count += 1
            dst_file = os.path.join(dest_directory, '%s-%d%s' % (basename, count, ext))
        # print 'Renaming %s to %s' % (file, dst_file)
        os.rename(os.path.join(file_directory, filename), dst_file)

    def manage_image(self, directory, filename, file_exif):
        basename, ext = os.path.splitext(filename)
        dest_name = self.extract_datetime(file_exif)
        if file_exif == {} or dest_name == "":
            dest_name,dest_directory = self.detect_file_date(directory,filename)
        else:
            match = re.search(r'(\d{4}):(\d{2}):(\d{2})', dest_name).groups()
            dest_directory = self.create_folder_if_not_exists(os.path.join(self.processed_folder, "regular",
                                                                                  repr(match[0]).replace("\\", "").replace("'",""),
                                                                                  months[int(match[1])-1]))
        self.move_file(directory, filename, dest_directory, (dest_name+ext).replace(":", "-"))

    def manage_non_image(self, directory, filename, file_type):
        if file_type == "video":
            dest_directory = self.create_folder_if_not_exists(os.path.join(self.processed_folder, "video"))
        else:
            dest_directory = self.create_folder_if_not_exists(os.path.join(self.processed_folder, "nonImage"))
        self.move_file(directory, filename, dest_directory, filename)

    def manage_duplicate_file(self, directory, filename, file_type):
        if file_type == "image":
            dest_directory = self.copy_directory_structure(directory, self.duplicate_folder)
        elif file_type == "video":
            dest_directory = self.copy_directory_structure(directory, os.path.join(self.duplicate_folder, "videos"))
        else:
            dest_directory = self.copy_directory_structure(directory, os.path.join(self.duplicate_folder, "otherd"))

        self.move_file(directory, filename, dest_directory, filename)

    def copy_directory_structure(self, directory_to_copy, directory_destination):
        new_directory = directory_to_copy.replace(self.root_path,"")
        new_directory = os.path.join(directory_destination,new_directory)
        self.create_folder_if_not_exists(new_directory)
        return new_directory

    def detect_file_date(self, directory, filename):
        final_name = ""
        dest_directory = ""
        possible_pattern = ["[January|February|March|April|May|June|July|August|September|October|November|December]*_[0-9]{2}__[0-9]*",
                            "([0-9]{4})([0-9]{2})([0-9]{2})[-_]([0-9]*)",#Année#mois#jour#serie
                            "([0-9]{2})([0-9]{2})([0-9]{2})[-_]([0-9]*)",#mois#Année#jour#serie
                            "([0-9]{4})[-_]([0-9]{2})[-_]([0-9]{2})[\-\s]([0-9]{2})[h\:\-\s\.]([0-9]{2})[m\:\-\s\.]([0-9]{2})",#année mois jour heure minutes secondes
                            "([0-9]{2})[-_]([0-9]{2})[-_]([0-9]{2})[\-\s]([0-9]{2})[h\:\-\s\.]([0-9]{2})[m\:\-\s\.]([0-9]{2})",#année mois jour heure minutes secondes
                            ]
        for pattern in possible_pattern:
            matches = re.match(pattern,final_name)
            if(matches != None):
                print(matches.groups())
        #Last chance : get filesystem creation date
        if final_name == "":
            match = time.gmtime(os.path.getmtime(os.path.join(directory, filename)))
            final_name = repr(match[0]) + ":" + repr(match[1]) + ":" + repr(match[2]) + "_" + repr(
                        match[3]) + ":" + repr(match[4]) + ":" + repr(match[5])
            dest_directory = self.create_folder_if_not_exists(os.path.join(self.processed_folder, "emptyExif",repr(match[0]),repr(match[1]),repr(match[2])))
        return final_name,dest_directory