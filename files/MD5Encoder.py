import os, hashlib


class MD5Encoder:
    m_database_path = None

    def __init__(self,database_location):
        self.m_database_path = os.path.join(database_location, "database.txt")
        file = open(self.m_database_path, "a", 1)
        file.close()

    def hash_file(self,file):
        hash_md5 = hashlib.md5()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def is_file_already_present(self,file):
        hashed_file = self.hash_file(file)
        f = open(self.m_database_path)
        contents = f.read()
        f.close()
        return contents.count(hashed_file) > 0

    def add_hash_in_database(self, hash, fileName):
        file = open(self.m_database_path, "a", 1)
        file.write(hash)
        file.write(' ('+fileName+ ')')
        file.write("\n\r")
        file.close()
