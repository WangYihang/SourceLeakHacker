import sys
import queue
import threading
import time
import requests
from multiprocessing import JoinableQueue

from lib.util import logger
from lib.util import terminal
from lib.context import context


def check(url, timeout, retry=4):
    try:
        start_time = time.time()
        response = requests.head(url, timeout=timeout)
        end_time = time.time()

        code = response.status_code
        if "Content-Length" in response.headers:
            content_length = response.headers["Content-Length"]
        else:
            content_length = "0"
        if "Content-Type" in response.headers:
            content_type = response.headers["Content-Type"]
        else:
            content_type = "UNKNOWN"
        time_used = end_time - start_time

        context.result[url] = {
            "code":code,
            "headers":response.headers,
            "time":time_used,
            "Content-Length": content_length,
            "Content-Type": content_type,
        }
        logger.http("[%d]\t%s\t%02f\t%s\t%s" % (code, content_length, time_used, content_type, url), code)
    except Exception as e:
        logger.detail(e)
        raise e

class Producer(threading.Thread):
    def __init__(self, Q, urls, foldernames_file, filenames_file, backups_file, timeout):
        threading.Thread.__init__(self)
        # self.daemon = True
        self.Q = Q
        self.urls = urls
        self.foldernames_file = foldernames_file
        self.filenames_file = filenames_file
        self.backups_file = backups_file
        self.timeout = timeout

    def run(self):
        # Generate tasks for threads
        foldernames = [i.strip() for i in list(self.foldernames_file)][0:3]
        filenames = [i.strip() for i in list(self.filenames_file)][0:3]
        backups = [i.strip() for i in list(self.backups_file)][0:3]
        paths = []
        for folder in foldernames:
            for filename in filenames:
                for backup in backups:
                    paths.append("{}{}".format(folder, backup.replace("?", filename)))
        for path in paths:
            for url in self.urls:
                u = "{}{}".format(url, path)
                task = {"url":u, "timeout": self.timeout, "retry":4}
                if not context.CTRL_C_FLAG:
                    self.Q.put(task)
        context.FINISH_FLAG = True


class Consumer(threading.Thread):
    def __init__(self, Q):
        threading.Thread.__init__(self)
        self.daemon = True
        self.Q = Q

    def run(self):
        while True:
            if self.Q.qsize() == 0 and context.FINISH_FLAG:
                break
            task = self.Q.get()
            try:
                check(task["url"], task["timeout"])
            except Exception as e:
                # retry may cause dead lock, so disabled
                # if task["retry"] > 0:
                #     task["retry"] -= 1
                #     self.Q.put(task)
                # print("{}, eescheduling task: {}".format(repr(e), task))
                pass

            finally:
                # Mark this task as done, whether an exception happened or not
                self.Q.task_done()

def start(urls, foldernames_file, filenames_file, backups_file, threads_number, timeout):
    Q = queue.Queue(maxsize=threads_number * 2)

    producer = Producer(Q, urls, foldernames_file, filenames_file, backups_file, timeout)
    producer.start()

    for i in range(threads_number):
        consumer = Consumer(Q)
        consumer.start()
        
    producer.join()
