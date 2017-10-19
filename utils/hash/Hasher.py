import errno
import hashlib
import logging

logger = logging.getLogger(__name__)


def hash_file(file_type, file):
    if hasattr(hashlib, file_type):
        method_to_call = getattr(hashlib, file_type)
        hash_md5 = method_to_call()
    else:
        hash_md5 = hashlib.md5()
    try:
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except OSError as e:
        if e.errno == errno.ENOENT:
            logger.info(file + " Not Found continuing")
    return ""
