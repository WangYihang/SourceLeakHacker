#!/usr/bin/env python
# encoding:utf-8

import threading
import requests
import signal
import sys

from colorama import init as initcolorama
from lib.util import logger
from lib.util import url
from lib.util import output
from lib.util import signal as sg
from lib.info import prompt
from lib.core import spider
from lib.core import dispatcher


def init():
    initcolorama()
    initSignal()

def initSignal():
    signal.signal(signal.SIGINT, sg.ctrlC)
    signal.signal(signal.SIGTERM, sg.ctrlC)

def main():
    init()

    # Parse params
    if len(sys.argv) != 4:
        prompt.show(sys.argv[0])
        exit(1)

    website = url.urlFormater(sys.argv[1])
    threadNumber = int(sys.argv[2])
    timeout = float(sys.argv[3])
    if timeout == 0:
        logger.error("[-] Your timeout can not be equal with 0!")
        prompt.show(sys.argv[0])
        exit(1)
    listFile = open('list.txt', 'r')
    dispatcher.start(website, threadNumber, listFile, timeout)
    output.asTable()
    output.asCSV("result.csv")

if __name__ == "__main__":
    main()
