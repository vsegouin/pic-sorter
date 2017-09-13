import logging
import mimetypes
import os

from utils.constants import MIMES_TYPES

logger = logging.getLogger(__name__)

particular_case = {os.path.sep + '.git' + os.path.sep: MIMES_TYPES.GIT,
                   os.path.sep + '.idea' + os.path.sep: MIMES_TYPES.IDEA,
                   os.path.sep + 'node_modules' + os.path.sep: MIMES_TYPES.NODE_MODULES}


def detect_image_file(file):
    type = mimetypes.guess_type(file)[0]
    logger.debug(type)
    if any(particular in file for particular in particular_case.keys()):
        for p in particular_case.keys():
            if p in file:
                return particular_case.get(p)
    return MIMES_TYPES.mimes_list.get(type, {"group": MIMES_TYPES.OTHER}).get('group')
