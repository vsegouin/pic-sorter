import mimetypes

from utils.Logger import Logger

logger = Logger()
def detect_image_file(file):
    type = mimetypes.guess_type(file)[0]
    if type == None:
        return "other"
    logger.log(type)
    if "image/" in type:
        return "image"
    if "image/" in type:
        return "video"
    return "other"
