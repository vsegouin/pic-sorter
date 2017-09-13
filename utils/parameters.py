import logging
import platform, argparse
import os


class Parameters:
    reset_database = False
    is_verbose = False
    dry_run = False
    is_windows = platform.system() == "Windows"
    log_level = logging.INFO

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--verbose', help='Set the program on verbose mode', action='store_true')
        parser.add_argument('--dry-run', help='Set the program on dry run mode', action='store_true')
        parser.add_argument('--reset-database', help='reset the database when running', action='store_true')
        parser.add_argument('root_path', help='Path to sort', metavar="root of path to sort")
        args = parser.parse_args()
        PATHS.load_paths(args)
        Parameters.load_params(args)

    @staticmethod
    def load_params(args):
        Parameters.is_verbose = args.verbose
        Parameters.dry_run = args.dry_run
        Parameters.reset_database = args.reset_database

        if Parameters.is_verbose:
            Parameters.log_level = logging.DEBUG

class PATHS:
    root_path = ""
    md5_database_path = ""
    duplicate_folder = ""
    processed_folder = ""

    @staticmethod
    def load_paths(args):
        PATHS.root_path = args.root_path
        PATHS.md5_database_path = os.path.join(PATHS.root_path, "database.txt")
        PATHS.duplicate_folder = os.path.join(PATHS.root_path, "duplicate")
        PATHS.processed_folder = os.path.join(PATHS.root_path, "processed")


def show_parameters():
    PATHS_attr = [attr for attr in dir(PATHS) if not callable(getattr(PATHS, attr)) and not attr.startswith("__")]
    Parameters_attr = [attr for attr in dir(Parameters) if
                       not callable(getattr(Parameters, attr)) and not attr.startswith("__")]
    logger = logging.getLogger(__name__)
    for i in PATHS_attr:
        logger.info(i + ' : ' + repr(getattr(PATHS, i)))
    for a in Parameters_attr:
        logger.info(a + ' : ' + repr(getattr(Parameters, a)))
