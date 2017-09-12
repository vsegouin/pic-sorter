from utils.reporting import Reporting

#@todo: REFACTOR !!!
def manage_duplicate_file(self, directory, filename, file_type):
    Reporting.duplicate_found += 1
    if file_type == "image":
        dest_directory = self.copy_directory_structure(directory, self.duplicate_folder)
    elif file_type == "video":
        dest_directory = self.copy_directory_structure(directory, os.path.join(self.duplicate_folder, "video"))
    else:
        dest_directory = self.copy_directory_structure(directory, os.path.join(self.duplicate_folder, "other"))

    self.move_file(directory, filename, dest_directory, filename)

