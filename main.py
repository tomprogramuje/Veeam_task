""" Folder synchronization script

This script allows the user to synchronize two folders to maintain a full,
identical copy of source folder at destination folder.

This tool accepts CLI arguments specifying the source and destination folder
of the synchronization, path where the log_file will be created/updated
and interval of the synchronization.

This script requires no extra packages to be installed within the Python
environment you are running this script in, as it only uses standard library.
"""

import os
import shutil
import filecmp
import datetime
import time
import argparse


def remove_file(file, dst, log_path):
    """
    Removes a file from destination folder and logs the operation
    :param file: name of the file to be removed
    :type file: str
    :param dst: location of the synchronization destination folder from which the file will be deleted from
    :type dst: str
    :param log_path: location of the log file
    :type log_path: str
    :return: None
    """

    dst_file = os.path.join(dst, file)
    os.remove(dst_file)
    log(log_path, "removed from", file)


def add_file(file, src, dest, log_path):
    """
    Copies a new file created in source folder to destination folder
    and logs the operation
    :param file: name of the file that was created
    :type file: str
    :param src: location of the synchronization source folder in which the file was created
    :type src: str
    :param dest: location of the synchronization destination folder to which the file will be copied to
    :type dest: str
    :param log_path: location of the log file
    :type log_path: str
    :return: None
    """

    src_file = os.path.join(src, file)
    shutil.copy2(src_file, dest)
    log(log_path, "added to", file)


def update_file(file, src, dest, log_path):
    """
    Removes a file from destination folder and copies an updated file from
    source to destination folder, then logs the operation
    :param file: name of the file that was updated
    :type file: str
    :param src: location of the synchronization source folder in which the file was updated
    :type src: str
    :param dest: location of the synchronization destination folder to which the file will be copied to
    :type dest: str
    :param log_path: location of the log file
    :type log_path: str
    :return: None
    """

    src_file = os.path.join(src, file)
    dest_file = os.path.join(dest, file)
    if not filecmp.cmp(src_file, dest_file):
        os.remove(dest_file)
        shutil.copy2(src_file, dest)
        log(log_path, "updated in", file)


def log(log_path, action, file):
    """
    Provides logging functionality to above functions, logs an operation
    made in/on destination folder to a provided logfile and prints
    the same information on console
    :param log_path: location of the log file
    :type log_path: str
    :param action: message describing actions that were taken upon source and destination folders
    :type action: str
    :param file: name of the file that was updated
    :type file: str
    :return: None
    """

    msg = f"\n{datetime.datetime.now().replace(microsecond=0)} File {file} has been {action} source folder, destination folder has been synchronized."
    print(msg)
    f = open(f"{log_path}\sync_log.txt", "a")
    f.write(f"\n{msg}")
    f.close()


def main():
    """
    Provides the means to accept CLI arguments and calls functions
    neccesary for synchronizing the provided folders and
    logging the operations in requested frequency
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "src", help="specifies the source folder path for synchronizing"
    )
    parser.add_argument(
        "dest", help="specifies the destination folder path for synchronizing"
    )
    parser.add_argument(
        "log_path", help="specifies the folder path for logging synchronization"
    )
    parser.add_argument(
        "sync_interval", help="specifies the synchronization interval", type=int
    )
    args = parser.parse_args()

    while True:
        src_files = set(os.listdir(args.src))
        dest_files = set(os.listdir(args.dest))

        removed_files = dest_files - src_files
        added_files = src_files - dest_files
        common_files = src_files.intersection(dest_files)

        for file in added_files:
            add_file(file, args.src, args.dest, args.log_path)

        for file in removed_files:
            remove_file(file, args.dest, args.log_path)

        for file in common_files:
            update_file(file, args.src, args.dest, args.log_path)

        time.sleep(args.sync_interval)


if __name__ == "__main__":
    main()
