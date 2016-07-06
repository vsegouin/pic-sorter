import platform


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# Python2
class Parameters(object):
    is_verbose = False
    root_path = ""
    dry_run = False

    is_windows = platform.system() == "Windows"
    __metaclass__ = Singleton

    def Parameters(self):
        pass
