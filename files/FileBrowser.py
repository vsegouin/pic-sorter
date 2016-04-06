import glob, os


class FileBrowser:
    m_folder_path = None
    m_list_directory = []
    m_list_file = []

    def __init__(self, folder_path):
        self.m_folder_path = folder_path

    def list_file(self):
        os.chdir(self.m_folder_path)  # change directory
        for file in glob.glob("*[^.txt]"):  # list all file in directory
            if(os.path.isdir(file)):
                self.m_list_directory.append(os.path.join(self.m_folder_path, file))
            else:
                self.m_list_file.append(os.path.join(self.m_folder_path, file))
