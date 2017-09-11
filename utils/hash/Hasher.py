import hashlib
from utils.Logger import Logger
import errno

logger = Logger()


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
            logger.log(file + " Not Found continuing")
    return ""
