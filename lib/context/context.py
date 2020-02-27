import threading

screenLock = threading.Semaphore(value=1)
result = dict()
CTRL_C_FLAG = False
FINISH_FLAG = False