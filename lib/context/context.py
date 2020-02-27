import threading

screenLock = threading.Semaphore(value=1)

result = dict()
result_lock = threading.Lock()

foldernames_cache = dict()
foldernames_lock = threading.Lock()
filenames_cache = dict()
filenames_lock = threading.Lock()
backups_cache = dict()
backups_lock = threading.Lock()

CTRL_C_FLAG = False
FINISH_FLAG = False

foldernames_dictionary = "folders.txt"
filenames_dictionary = "files.txt"
backups_dictionary = "backups.txt"

statistic = dict()
statistic_lock = threading.Lock()