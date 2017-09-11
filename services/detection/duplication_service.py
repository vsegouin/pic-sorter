# Return true if Hash code is not blank and it's not present in database.txt
from utils.files.file_writer import write_in_file
from utils.parameters import PATHS


def is_file_already_present(type, md5_hash):
    f = open(PATHS.md5_database_path)
    contents = f.read()
    f.close()
    return True if md5_hash == "" or contents.count(md5_hash) > 0 else False


def add_hash_to_database(md5_hash):
    write_in_file(PATHS.md5_database_path, md5_hash)
