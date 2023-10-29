import os
import shutil
import filecmp

"""
- Synchronization must be one-way: after the synchronization content of the
 replica folder should be modified to exactly match content of the source
 folder - done
- Synchronization should be performed periodically
- File creation/copying/removal operations should be logged to a file and to the
 console output - done
- Folder paths, synchronization interval and log file path should be provided
 using the command line arguments
"""

"""
remove_file removes a file from destination folder
"""
def remove_file(file, dst, log_path):
    dst_file = os.path.join(dst, file)
    os.remove(dst_file)


"""
add_file adds new file to destination folder
"""
def add_file(file, src, dst, log_path):
    src_file = os.path.join(src, file)
    shutil.copy2(src_file, dst)


"""
update_file updated a file in destination folder
"""
def update_file(file, src, dst, log_path):
    src_file = os.path.join(src, file)
    dst_file = os.path.join(dst, file)
    if not filecmp.cmp(src_file, dst_file):
        os.remove(dst_file)
        shutil.copy2(src_file, dst)


"""
log logs an operation made in/on destination folder to provided logfile and prints the same information on console
"""
def log(path, action, file):
    print(f"File {file} has been {action} destination folder")
    f = open(f"{path}\log.txt", "a")
    f.write(f"File {file} has been {action} destination folder\n")
    f.close()


"""
main routine 
"""
def main():
    src = r"C:\Users\tomse\Dropbox\Python\Veeam_task\src"
    dst = r"C:\Users\tomse\Dropbox\Python\Veeam_task\replica"
    log_path = r"C:\Users\tomse\Dropbox\Python\Veeam_task"

    src_files = set(os.listdir(src))
    dst_files = set(os.listdir(dst))

    removed_files = dst_files - src_files
    added_files = src_files - dst_files
    common_files = src_files.intersection(dst_files)

    for file in added_files:
        add_file(file, src, dst, log_path)
        log(log_path, "added to", file)

    for file in removed_files:
        remove_file(file, dst, log_path)
        log(log_path, "removed from", file)

    for file in common_files:
        update_file(file, src, dst, log_path)
        log(log_path, "updated in", file)

if __name__ == "__main__":
    main()
