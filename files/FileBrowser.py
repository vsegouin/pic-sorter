import os

from Reporting import Reporting


class FileBrowser:
    root_path = None

    def __init__(self, root_path):
        self.root_path = root_path

    def count_processed_file(self):
        Reporting.total_file = 0
        Reporting.calculated_total_file = 0
        for root, subdirs, files in self.crawl_processed_folder():
            Reporting.calculated_total_file += files.__len__()

    def count_total_find(self):
        Reporting.total_file = 0
        Reporting.calculated_total_file = 0
        for root, subdirs, files in self.crawl_folders():
            Reporting.calculated_total_file += files.__len__()

    # Will crawl and generate all the files of the root_path
    def crawl_folders(self):
        for root, subdirs, files in os.walk(self.root_path):
            Reporting.log('-- current directory = ' + root + "\n")
            if ("@eaDir" in root):
                Reporting.log("it's a eadir folder continue\n")
                continue
            if "processed" in root or "duplicate" in root:
                Reporting.log("it's the processed or the duplicate folder skip")
                continue

            yield [root, subdirs, files]
            # check whether the directory is now empty after deletions, and if so, remove it
            if len(os.listdir(root)) == 0:
                os.rmdir(root)

    def crawl_processed_folder(self):
        for root, subdirs, files in os.walk(self.root_path):
            if not "processed" in root:
                continue
            yield [root, subdirs, files]

    def getPath(self):
        return self.root_path;
