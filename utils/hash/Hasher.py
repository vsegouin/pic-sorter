import hashlib
import errno
import logging
logger = logging.getLogger(__name__)


def hash_file(type,file):
    hash_md5 =''
    if 'sha1' == type:
        hash_md5 = hashlib.sha1()
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
