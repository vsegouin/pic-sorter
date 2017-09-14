import logging
import platform, argparse
import os

from watchdog.utils.bricks import OrderedSet

from utils.constants import MODE


class Parameters:
    application_mode = None
    reset_database = False
    can_remove = True
    is_verbose = False
    dry_run = False
    show_progress = False
    is_windows = platform.system() == "Windows"
    log_level = logging.INFO
    hash_modes = []
    report = False

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--verbose', help='Set the program on verbose mode', action='store_true')
        parser.add_argument('--remove', help='Set the program on remove mode', action='store_true')
        parser.add_argument('--dry-run', help='Set the program on dry run mode', action='store_true')
        parser.add_argument('--reset-database', help='reset the database when running', action='store_true')
        parser.add_argument('--root-path', help='Path to sort', metavar="root_path", nargs='?')
        parser.add_argument('--dedup', help='path containing duplicate / path to check',
                            metavar=('duplicate_folder', 'check_folder'), nargs='+')
        parser.add_argument('--hash-modes', help='hashes used', nargs='+', metavar="", default=['md5', 'sha1'])
        parser.add_argument('--show-progress', help='Show the progression', action='store_true')
        parser.add_argument('--report', help='Show reporting data at the end', action='store_true')

        args = parser.parse_args()
        Parameters.validate_parameters(args, parser)

        Parameters.load_params(args)
        PATHS.load_paths(args)

    @staticmethod
    def validate_parameters(args, parser):
        if not ((args.dedup is None) != (args.root_path is None)):
            parser.error('dedup and root-path arguments shouldn\'t be given at the same time')
        if args.dedup is not None and len(args.dedup) < 2:
            parser.error('dedup must be composed of at least TWO arguments')

        if args.dedup is not None:
            # Check path exists
            for i in args.dedup:
                if not os.path.isdir(i):
                    parser.error(i + ' doesn\'t exists')
            # Check path unicity
            for i in range(0, len(args.dedup)):
                for a in range(i + 1, len(args.dedup)):
                    if args.dedup[i] in args.dedup[a]:
                        parser.error(
                            " arg " + repr(a) + " : " + args.dedup[a] + ' contained in ' + repr(i) + ' : ' + args.dedup[
                                i])

        if args.root_path is not None:
            if not os.path.isdir(args.root_path):
                parser.error(args.root_path + ' doesn\'t exists')

    @staticmethod
    def get_application_mode(args):
        if args.root_path is not None:
            return MODE.SORTER
        if args.dedup is not None:
            return MODE.DEDUP

    @staticmethod
    def load_params(args):
        Parameters.is_verbose = args.verbose
        Parameters.dry_run = args.dry_run
        Parameters.report = args.report
        Parameters.reset_database = args.reset_database
        Parameters.application_mode = Parameters.get_application_mode(args)
        Parameters.can_remove = args.remove
        print('MODE : ' + Parameters.application_mode)
        for hash in args.hash_modes:
            Parameters.hash_modes.append(hash)
        print(Parameters.hash_modes)
        if Parameters.is_verbose:
            Parameters.log_level = logging.DEBUG


class PATHS:
    report_file_path = ""
    hash_databases = {}
    sha1_database_path = None
    root_path = None
    dedup_path = None
    md5_database_path = ""
    duplicate_folder = ""
    processed_folder = ""

    @staticmethod
    def load_paths(args):
        PATHS.root_path = args.root_path
        PATHS.dedup_path = args.dedup
        print(PATHS.dedup_path)
        base_path = PATHS.fetch_base_path(args)
        PATHS.duplicate_folder = os.path.join(base_path, "duplicate")
        PATHS.processed_folder = os.path.join(base_path, "processed")
        PATHS.report_file_path = os.path.join(base_path,'reporting.txt')
        for hash in Parameters.hash_modes:
            PATHS.hash_databases.update({hash: os.path.join(base_path, 'database.' + hash + '.txt')})
        print(PATHS.hash_databases)

    @staticmethod
    def fetch_base_path(args):
        if args.root_path is not None:
            return args.root_path
        else:
            return args.dedup[0]


def show_parameters():
    PATHS_attr = [attr for attr in dir(PATHS) if not callable(getattr(PATHS, attr)) and not attr.startswith("__")]
    Parameters_attr = [attr for attr in dir(Parameters) if
                       not callable(getattr(Parameters, attr)) and not attr.startswith("__")]
    logger = logging.getLogger(__name__)
    for i in PATHS_attr:
        logger.info(i + ' : ' + repr(getattr(PATHS, i)))
    for a in Parameters_attr:
        logger.info(a + ' : ' + repr(getattr(Parameters, a)))

