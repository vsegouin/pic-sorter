import mimetypes

import exifread
import magic
from mimetypes import MimeTypes

class ExifReader:
    def __init__(self):
        pass

    def read_exif(self, file):
        f = open(file, 'rb')
        # Return Exif tags
        tags = exifread.process_file(f)
        return tags

    def is_image(self,file):
        type = mimetypes.guess_type(file)[0]
        return True if type != None and "image/" in type else False

    def is_video(self,file):
        type = mimetypes.guess_type(file)[0]
        return True if type != None and "video/" in type else False