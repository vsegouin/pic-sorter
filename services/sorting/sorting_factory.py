# coding=utf-8
from services.sorting import image_sorting
from utils.constants import MIMES_TYPES


def manage_file(file_path, mimes_type):
    if mimes_type == MIMES_TYPES.IMAGE:
        return image_sorting.sort_image(file_path)


# @todo:REFACTOR
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
        Reporting.unmovable_file.append(os.path.join(directory, filename))
