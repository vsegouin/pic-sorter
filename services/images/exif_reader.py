import mimetypes

import exifread


def read_exif(file):
    f = open(file, 'rb')
    try:
        tags = exifread.process_file(f)
    except TypeError:
        tags = ''
    return tags
