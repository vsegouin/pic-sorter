from files.MD5Encoder import MD5Encoder
import os
import sys

root_path = sys.argv[1]

# init database.txt in root_path
md5enc = MD5Encoder(root_path)

print('walk_dir = ' + root_path+"\n")

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(root_path)+"\n")
total_file_number = 0;
total_file_number_processed = 0;
for root, subdirs, files in os.walk(root_path):
    file_number = 0
    file_processed = 0
    print('-- current directory = ' + root + "\n")
    if("@eaDir" in root):
        print("it's a eadir folder continue\n")
        continue

    for filename in files:
        file_number += 1
        file_path = os.path.join(root, filename)
        md5enc.init_file(file_path)
        if not md5enc.is_file_already_present() and file_path != os.path.join(root_path, "database.txt"):
            file_processed += 1
            md5enc.add_hash_in_database()
        else :
            pass
    total_file_number += file_number
    total_file_number_processed += file_processed
    print("there was " + repr(file_number) + " in " + repr(root) + " and "+repr(file_processed)+" has been processed\n")

print("At the end there was "+repr(total_file_number)+" and "+repr(total_file_number_processed)+" processed\n\nEND PROGRAM \n\n")