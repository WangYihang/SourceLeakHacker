import sys
import queue
import threading
import time
import requests

from colorama import Style
from lib.util import color
from lib.util import terminal
from lib.context import context

def check(url, foldername, filename, backup, timeout=4):
    try:
        start_time = time.time()
        response = requests.head(url, timeout=timeout, verify=False)
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

        context.result_lock.acquire()
        context.result[url] = {
            "code":code,
            "headers":response.headers,
            "time":time_used,
            "Content-Length": content_length,
            "Content-Type": content_type,
        }
        context.result_lock.release()

        context.statistic_lock.acquire()
        if code not in context.statistic.keys():
            context.statistic[code] = 0
        context.statistic[code] += 1
        context.statistic_lock.release()

        # Update cache
        if code >= 200 and code < 300:
            context.foldernames_lock.acquire()
            context.foldernames_cache[foldername] += 1
            context.foldernames_lock.release()

            context.filenames_lock.acquire()
            context.filenames_cache[filename] += 1
            context.filenames_lock.release()

            context.backups_lock.acquire()
            context.backups_cache[backup] += 1
            context.backups_lock.release()

        context.screenLock.acquire()
        print(color.projection(code) + "[%d]\t%s\t%02f\t%s\t%s" % (code, content_length, time_used, content_type, url))
        print(Style.RESET_ALL, end="")
        context.screenLock.release()
    except Exception as e:
        code = 0
        context.result_lock.acquire()
        context.result[url] = {
            "code":code,
            "time":0,
            "Content-Length": 0,
            "Content-Type": repr(e).replace(",", "|"),
        }
        context.result_lock.release()
        context.logger.error(e)

        context.statistic_lock.acquire()
        if code not in context.statistic.keys():
            context.statistic[code] = 0
        context.statistic[code] += 1
        context.statistic_lock.release()

        raise e

class Producer(threading.Thread):
    def __init__(self, Q, urls, foldernames_file, filenames_file, backups_file, timeout):
        threading.Thread.__init__(self)
        self.daemon = True
        self.Q = Q
        self.urls = urls
        self.foldernames_file = foldernames_file
        self.filenames_file = filenames_file
        self.backups_file = backups_file
        self.timeout = timeout

    def run(self):
        # Generate tasks for threads
        context.logger.info("Loading dictionaries: 1/3")
        for i in list(self.foldernames_file):
            key = i.split("\t")[1].strip()
            value = int(i.split("\t")[0])
            context.foldernames_lock.acquire()
            context.foldernames_cache[key] = value
            context.foldernames_lock.release()

        context.logger.info("Loading dictionaries: 2/3")
        for i in list(self.filenames_file):
            key = i.split("\t")[1].strip()
            value = int(i.split("\t")[0])
            context.filenames_lock.acquire()
            context.filenames_cache[key] = value
            context.filenames_lock.release()

        context.logger.info("Loading dictionaries: 3/3")
        for i in list(self.backups_file):
            key = i.split("\t")[1].strip()
            value = int(i.split("\t")[0])
            context.backups_lock.acquire()
            context.backups_cache[key] = value
            context.backups_lock.release()

        context.logger.info("Sorting dictionaries...")
        for backup in sorted(context.backups_cache.items(), key=lambda item:item[1], reverse=True):
            for foldername in sorted(context.foldernames_cache.items(), key=lambda item:item[1], reverse=True):
                for url in self.urls:
                    # Check folder existance
                    folder_url = "{}{}".format(url, foldername[0])
                    skip_flag = False
                    try:
                        response = requests.head(folder_url, timeout=self.timeout, verify=False)
                        code = response.status_code
                        if code >= 400 and code < 500:
                            skip_flag = True
                            context.logger.info("Folder({}) not exists, skipping scanning files in this folder.".format(folder_url))
                    except Exception as e:
                        context.logger.error(repr(e))

                    if skip_flag:
                        continue

                    for filename in sorted(context.filenames_cache.items(), key=lambda item:item[1], reverse=True):
                        path = "{}{}".format(foldername[0], backup[0].replace("?", filename[0]))
                        u = "{}{}".format(url, path)
                        task = {
                            "url":u, 
                            "timeout": self.timeout, 
                            "retry":4, 
                            "foldername": foldername[0], 
                            "filename":filename[0],
                            "backup": backup[0],
                        }
                        if not context.CTRL_C_FLAG:
                            self.Q.put(task)
                    if context.CTRL_C_FLAG: break
                if context.CTRL_C_FLAG: break
            if context.CTRL_C_FLAG: break

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
                check(task["url"], task["foldername"], task["filename"], task["backup"], task["timeout"])
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

    producer = Producer(Q, urls, open(foldernames_file), open(filenames_file), open(backups_file), timeout)
    producer.start()

    for i in range(threads_number):
        consumer = Consumer(Q)
        consumer.start()

    producer.join()
