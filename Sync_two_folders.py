"""Please implement a program that synchronizes two folders: source and replica. The program should maintain a full,
identical copy of source folder at replica folder.
Solve the test task by writing a program in Python language.
Synchronization must be one-way: after the synchronization content of the replica folder should be modified to exactly
match content of the source folder;
Synchronization should be performed periodically.
File creation/copying/removal operations should be logged to a file and to the console output; Folder paths, synchronization
interval and log file path should be provided using the command line arguments;
It is undesirable to use third-party libraries that implement folder synchronization;
It is allowed (and recommended) to use external libraries implementing other well-known algorithms. For example, there
is no point in implementing yet another function that calculates MD5 if you need it for the task – it is perfectly acceptable
to use a third-party (or built-in) library."""


import argparse
import hashlib
import logging
import os
import shutil
import sys
import time


SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
print(f"SCRIPT DIRE PATH = {SCRIPT_DIR_PATH}")


# setting up argument parser
def get_parser():
    parser = argparse.ArgumentParser(description='Argument parser for folder synchronization script.')
    parser.add_argument('-s', '--source', type=str, default=os.path.join(SCRIPT_DIR_PATH, 'source_dir'), help='Path to the source directory.')
    parser.add_argument('-r', '--replica', type=str, default=os.path.join(SCRIPT_DIR_PATH, 'replica_dir'), help='Path to the replica directory.')
    parser.add_argument('-l', '--logfile', type=str, default=os.path.join(SCRIPT_DIR_PATH, 'logfile.txt'), help='Path to logfile.')
    parser.add_argument('-t', '--timesleep', type=int, default=2, help='Sleep time in seconds (default: 2).')

    args = parser.parse_args()
    return args


# comparing files with hash
def compare_files(file1, file2):
    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            if hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest():
                return True
            else:
                return False


# comparing source folder with replica folder
def compare_folders(source, replica):
    files_source = os.listdir(source)
    files_replica = os.listdir(replica)
    if len(files_source) != len(files_replica):
        return False

    for file in files_source:
        if file in files_replica:
            source_file_path = os.path.join(source, file)
            replica_file_path = os.path.join(replica, file)
            if os.path.isfile(source_file_path) and os.path.isfile(replica_file_path) and not compare_files(source_file_path, replica_file_path):
                return False
        else:
            return False
    return True


# handling source and replica directories state
def handle_directories(source_dir, replica_dir):
    synchronized_no_of_files = 0
    created_no_of_files = 0
    updated_no_of_files = 0
    deleted_no_of_files = 0

    # get files in source and replica
    files_source = os.listdir(source_dir)
    files_replica = os.listdir(replica_dir)

    # parse files in replica to check if needs updating or removing
    for file in files_replica:
        replica_file_path = os.path.join(replica_dir, file)
        source_file_path = os.path.join(source_dir, file)
        if file in files_source:
            if compare_files(source_file_path, replica_file_path):
                logging.info(f">>{file} is already up to date")
                synchronized_no_of_files += 1

            else:
                updated_no_of_files += 1
                os.remove(replica_file_path)
                shutil.copy(os.path.join(source_dir, file), os.path.join(replica_dir, file))
                logging.info(f'>>{file} is updated')

        else:  # if file not in files_source:
            logging.info(f'>>{file} is deleted')
            deleted_no_of_files += 1
            os.remove(replica_file_path)

    for file in files_source:
        if file not in files_replica:
            created_no_of_files += 1
            logging.info(f'>>{file} is created')
            shutil.copy(os.path.join(source_dir, file), os.path.join(replica_dir, file))

    total_no_of_files = synchronized_no_of_files + created_no_of_files + updated_no_of_files + deleted_no_of_files
    logging.info(f'(total no of files analysed: {total_no_of_files}) synced: {synchronized_no_of_files}; created: {created_no_of_files}; updated: {updated_no_of_files}; deleted: {deleted_no_of_files}')


def main():
    args = get_parser()
    source = args.source
    replica = args.replica
    time_sleep = args.timesleep
    logfile = args.logfile

    # setting up the log
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)-8s %(name)-6s %(message)s",
                        handlers=[logging.FileHandler(logfile), logging.StreamHandler(sys.stdout)])


    logging.info("Starting our sync folder script...")

    # checking if replica dir exists
    if not (os.path.exists(replica) and os.path.isdir(replica)):
        logging.error(f"Replica dir {replica} has been created.")
        os.mkdir(replica)

    if not os.path.isdir(source):
        logging.error(f"Source dir {source} is not a directory...")
    else:
        while True:
            if compare_folders(source, replica):
                logging.info("Source dir and replica dir are matching / up to date one with the other....")

            else:
                logging.info("Source dir and replica are not matching...")
                handle_directories(source, replica)
            time.sleep(time_sleep)
            logging.info(f"Sleeped for {time_sleep} seconds. Checking directories now..")


if __name__ == '__main__':
    main()
