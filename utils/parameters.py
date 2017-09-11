import platform, argparse
from utils.Logger import Logger
import os

logger = Logger()


class Parameters:
    is_verbose = False
    dry_run = False
    is_windows = platform.system() == "Windows"

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--verbose', help='Set the program on verbose mode', action='store_true')
        parser.add_argument('--dry-run', help='Set the program on dry run mode', action='store_true')
        parser.add_argument('root_path', help='Path to sort', metavar="root of path to sort")
        args = parser.parse_args()
        Parameters.is_verbose = args.verbose
        Parameters.dry_run = args.dry_run

        PATHS.root_path = args.root_path
        PATHS.md5_database_path = os.path.join(PATHS.root_path, "database.txt")
        PATHS.duplicate_folder = os.path.join(PATHS.root_path, "duplicate")
        PATHS.processed_folder = os.path.join(PATHS.root_path, "processed")


class PATHS:
    root_path = ""
    md5_database_path = ""
    duplicate_folder = ""
    processed_folder = ""


def show_parameters():
    PATHS_attr = [attr for attr in dir(PATHS) if not callable(getattr(PATHS, attr)) and not attr.startswith("__")]
    Parameters_attr = [attr for attr in dir(Parameters) if
                       not callable(getattr(Parameters, attr)) and not attr.startswith("__")]
    for i in PATHS_attr:
        logger.log(i + ' : ' + repr(getattr(PATHS, i)))
    for a in Parameters_attr:
        logger.log(a + ' : ' + repr(getattr(Parameters, a)))
