import PIL.ExifTags
import PIL.Image


class ExifReader:
    file_path = None

    def __init__(self, file_path):
        self.file_path = file_path

    def read_exif(self):
        img = PIL.Image.open(self.file_path)
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
            }

        return exif
