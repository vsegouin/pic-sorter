import os


class FileBrowser:
    total_file_number = 0;
    total_file_number_processed = 0;
    root_path = None

    def __init__(self, root_path):
        self.root_path = root_path

    # Will crawl and generate all the files of the root_path
    def crawl_folders(self):
        for root, subdirs, files in os.walk(self.root_path):
            print('-- current directory = ' + root + "\n")
            if ("@eaDir" in root):
                print("it's a eadir folder continue\n")
                continue
            if "processed" in root or "duplicate" in root:
                print("it's the processed or the duplicate folder skip")
                continue

            yield [root, subdirs, files]
