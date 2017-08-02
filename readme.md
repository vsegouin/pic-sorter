##PIC SORTER

Pic sorter is a python script created to crawl a folder and try to sort them depending on their MIME type
It will also move all the duplicated files in another folder.

I - Installation

    git clone https://github.com/vsegouin/pic-sorter.git
    cd pic-sorter
    python -m pip install requirements.txt
    
II - Usage


**WARNING**: This script can be dangerous if you don't use it properly, there is no rollback feature, i will not take any responsability in case of trouble, use it at your own risk.

    python path/to/__main__.py path/to/folder/to/sort

By default it will run a dry run and give a report about which files will be edited.

**You must delete database.txt between each run to avoid files to be considered as duplicate**

Then if you want to execute the actual run, you should use 
    
    python path/to/__main__.py path/to/folder/to/sort false
    
It will crawl all folders and subfolder recursively and will try to find duplicate and sorting your files.


III - How it works

It will hash each file in MD5 and store it in a file named database.txt
If a file is already presents it will move it in the "duplicate" folder
If it's not already presents, it will try to sort the file depending on it MIME type and will put it, sorted, in the "processed" folder.


