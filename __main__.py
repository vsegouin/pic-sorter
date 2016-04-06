from image.ExifReader import ExifReader
from files.FileBrowser import FileBrowser
from files.MD5Encoder import MD5Encoder

folderPath = "C:\\Users\\Vincent.Segouin\\Desktop\\photo"
fileBrow = FileBrowser(folderPath)
fileBrow.list_file()
md5enc = MD5Encoder("C:\\Users\\Vincent.Segouin\\Desktop\\photo")
for file in fileBrow.m_list_file:
    if not md5enc.is_file_already_present(file):
        md5enc.add_hash_in_database(md5enc.hash_file(file),file)
