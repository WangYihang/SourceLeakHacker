#!/usr/bin/env python
# encoding:utf-8

import threading
import requests
import signal
import sys
import time
import argparse

from colorama import init as initcolorama
from lib.util import logger
from lib.util import url
from lib.util import output
from lib.util import signal as sg
from lib.info import prompt
from lib.core import dispatcher

def init():
    initcolorama()
    initSignal()

def initSignal():
    signal.signal(signal.SIGINT, sg.ctrlC)
    signal.signal(signal.SIGTERM, sg.ctrlC)

def initArguments(output_filename):
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="url to scan, eg: 'http://127.0.0.1/'")
    group.add_argument("--urls", type=argparse.FileType("r"), help="file contains urls to sacn, one line one url.")

    parser.add_argument("--folders", type=argparse.FileType("r"), default="dict/folders.txt", help="dictionary for most common folder names")
    parser.add_argument("--files", type=argparse.FileType("r"), default="dict/files.txt", help="dictionary for most common file names")
    parser.add_argument("--backups", type=argparse.FileType("r"), default="dict/backups.txt", help="dictionary for most common backup file patterns")
    # parser.add_argument("--output", type=argparse.FileType("w"), default="result/{}.csv".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
    parser.add_argument("--output", default=output_filename, help="output csv filename")
    
    parser.add_argument("--threads", "-t", default=4, type=int, help="threads numbers, default: 4")
    parser.add_argument("--timeout", type=float, default=4, help="HTTP request timeout")

    parser.add_argument("--verbose", "-v", action="count", default=0, help="log level, eg: -vv")
    parser.add_argument("--version", "-V", action="version", version="%(prog)s 2.0")

    args = parser.parse_args()
    return args

def main():
    init()

    # Parse command line arguments
    output_filename = "result/{}.csv".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    args = initArguments(output_filename)

    # Parse urls
    urls = set()
    if args.url:
        urls = urls.union(url.Formater(args.url))
    if args.urls:
        for i in list(args.urls):
            x = url.Formater(i)
            urls = urls.union(x)

    # Start dispatching
    dispatcher.start(urls, args.folders, args.files, args.backups, args.threads,args.timeout)

    # Save result
    logger.plain("Result save in file: {}".format(output_filename))
    output.asCSV(args.output)

if __name__ == "__main__":
    main()
