import threading
import sys

from lib.util import logger
from lib.util import terminal
from lib.core import spider
from lib.context import context


def start(website, threadNumber, listFile, timeout):
    # Generate tasks for threads
    threads = []
    for i in listFile:
        i = i.replace("\n","")
        i = i.replace("\r","")
        if "?" in i:
            fileFile = open('file.txt', 'r')
            for j in fileFile:
                j = j.replace("\n","")
                j = j.replace("\r","")
                temp = i.replace("?",j)
                url = website + temp
                threads.append(spider.Spider(url, timeout))
        else:
            url = website + i
            threads.append(spider.Spider(url, timeout))
    
    logger.detail("%d tasks dispatched, starting threads..." % (len(threads)))

    # Start threads
    # counter = 0
    for thread in threads:
        if context.CTRL_C_FLAG:
            break
        # logger.detail("[%d / %d] Finished" % (counter, len(threads)))
        thread.start()
        thread.join()
        while True:
            if context.CTRL_C_FLAG:
                break
            # -1 for main thread
            if ((len(threading.enumerate()) - 1) < threadNumber):
                break
        # counter += 1

    
