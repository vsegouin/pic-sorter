import os


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

    def create_folder_if_not_exists(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
