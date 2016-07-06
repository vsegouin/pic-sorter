import mimetypes

import exifread


class ExifReader:
    def __init__(self):
        pass

    def read_exif(self, file):
        f = open(file, 'rb')
        # Return Exif tags
        try:
            tags = exifread.process_file(f)
        except TypeError or TypeError :
            tags = ''
        return tags

    def detect_image_file(self, file):
        type = mimetypes.guess_type(file)[0]
        if type == None:
            return "other"
        if "image/" in type:
            return "image"
        if "image/" in type:
            return "video"
        return "other"
