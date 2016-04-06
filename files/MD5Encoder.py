import os, hashlib


class MD5Encoder:
    m_database_path = ""
    m_current_file = ""
    m_hashed_value = ""

    def __init__(self,database_location):
        self.m_database_path = os.path.join(database_location, "database.txt")
        file = open(self.m_database_path, "a", 1)
        file.close()

    def init_file(self, file_path):
        self.m_current_file = file_path
        self.m_hashed_value = self.hash_file(file_path)

    def hash_file(self,file):
        self.m_current_file = file
        hash_md5 = hashlib.md5()
        try:
            with open(file, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except FileNotFoundError:
            print(file+" Not Found continuing")
        return ""

    def is_file_already_present(self):
        f = open(self.m_database_path)
        contents = f.read()
        f.close()
        print(self.m_current_file+" "+self.m_hashed_value)
        return True if self.m_hashed_value != "" and contents.count(self.m_hashed_value) > 0 else False

    def add_hash_in_database(self):
        file = open(self.m_database_path, "a", 1)
        file.write(self.m_hashed_value)
        file.write("\n\r")
        file.close()
