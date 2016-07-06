import os

from Reporting import Reporting


class FileBrowser:
    root_path = None

    def __init__(self, root_path):
        self.root_path = root_path
    def count_total_find(self):
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
