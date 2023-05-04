Hello!

This is my sync folders script written in Python.\
    1. The script will synchronize two folders: source and replica;\
    2. The program will maintain a full, identical copy of 
source folder at replica folder;\
    3. Synchronization will be one-way: after the synchronization, content of the replica folder will be modified to exactly
match content of the source folder;\
    4. Synchronization will be performed periodically;\
    5. File creation/copying/removal operations will be logged to a file and to the console output;\
    6. Folder paths, synchronization interval and log file path will be provided using the command line arguments.