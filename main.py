import os
import shutil

"""
- Synchronization must be one-way: after the synchronization content of the
 replica folder should be modified to exactly match content of the source
 folder - done
- Synchronization should be performed periodically
- File creation/copying/removal operations should be logged to a file and to the
 console output
- Folder paths, synchronization interval and log file path should be provided
 using the command line arguments
"""


def delete_files(src):
    for filename in os.listdir(src):
        src_file = os.path.join(src, filename)
        os.remove(src_file)
        print(f"{filename} have been deleted from the {src}(destination) folder")


def copy_files():
    src = input("Please provide the source directory you want to synchronize: ")
    dst = input("Please provide the destination directory you want to backup to: ")
    delete_files(dst)
    # should compare old list of files in src and new one
    file = open(f"{dst}\log.txt", "x")
    for filename in os.listdir(src):
        src_file = os.path.join(src, filename)
        shutil.copy2(src_file, dst)
        print(f"{filename} has been copied from {src} folder to {dst} folder")
        f = open(f"{dst}\log.txt", "a")
        f.write(f"{filename} has been copied from {src} folder to {dst} folder\n")
        f.close()


def log():
    pass

copy_files()

(r"C:\Users\tomse\Dropbox\Python\Veeam_task\src",)
(r"C:\Users\tomse\Dropbox\Python\Veeam_task\replica",)
src