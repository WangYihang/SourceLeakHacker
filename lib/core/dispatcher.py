import sys
import queue
import threading
import time
import requests
import prettytable

from lib.util import logger
from lib.util import terminal
from lib.context import context

def check(url, foldername, filename, backup, timeout=4):
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

        logger.http("[%d]\t%s\t%02f\t%s\t%s" % (code, content_length, time_used, content_type, url), code)
    except Exception as e:
        logger.detail("error:", e)
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
        for i in list(self.foldernames_file):
            key = i.split("\t")[1].strip()
            value = int(i.split("\t")[0])
            context.foldernames_lock.acquire()
            context.foldernames_cache[key] = value
            context.foldernames_lock.release()

        for i in list(self.filenames_file):
            key = i.split("\t")[1].strip()
            value = int(i.split("\t")[0])
            context.filenames_lock.acquire()
            context.filenames_cache[key] = value
            context.filenames_lock.release()

        for i in list(self.backups_file):
            key = i.split("\t")[1].strip()
            value = int(i.split("\t")[0])
            context.backups_lock.acquire()
            context.backups_cache[key] = value
            context.backups_lock.release()
        
        # Sort

        for foldername in list(context.foldernames_cache.keys()):
            for filename in list(context.filenames_cache.keys()):
                for backup in list(context.backups_cache.keys()):
                    path = "{}{}".format(foldername, backup.replace("?", filename))
                    for url in self.urls:
                        u = "{}{}".format(url, path)
                        task = {
                            "url":u, 
                            "timeout": self.timeout, 
                            "retry":4, 
                            "foldername": foldername, 
                            "filename":filename,
                            "backup": backup,
                        }
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


def save_dictionary(filename, dictionary):
    with open(filename, "w") as f:
        for k, v in dictionary.items():
            f.write("{}\t{}\n".format(v, k))


def start(urls, foldernames_file, filenames_file, backups_file, threads_number, timeout):
    Q = queue.Queue(maxsize=threads_number * 2)

    producer = Producer(Q, urls, open(foldernames_file), open(filenames_file), open(backups_file), timeout)
    producer.start()

    for i in range(threads_number):
        consumer = Consumer(Q)
        consumer.start()

    producer.join()
    
    logger.detail("Saving optimized dictionary: {}".format(foldernames_file))
    save_dictionary(foldernames_file, context.foldernames_cache)
    logger.detail("Saving optimized dictionary: {}".format(filenames_file))
    save_dictionary(filenames_file, context.filenames_cache)
    logger.detail("Saving optimized dictionary: {}".format(backups_file))
    save_dictionary(backups_file, context.backups_cache)
    
    # Print statistic information
    table = prettytable.PrettyTable()
    table.field_names = ["Code", "Times"]
    for k, v in context.statistic.items():
        table.add_row([k, v])
    table.set_style(prettytable.MSWORD_FRIENDLY)
    logger.plain(table)
