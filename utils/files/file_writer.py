import os

from utils.parameters import Parameters
from utils.reporting import Reporting


def write_all(self, list):
    file = open("test.txt", "a", 1)
    for item in list:
        file.write(item)
        file.write("\n\r")
    file.close()


def create_folder_if_not_exists(folder):
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

def write_in_file(file,text):
    file = open(file, "a", 1)
    file.write(text)
    file.write("\n\r")
    file.close()
