#!/usr/bin/env python
# encoding:utf-8

import threading
import requests
import signal
import sys
import glob
import time
import argparse

from colorama import init as initcolorama
from lib.util import logger
from lib.util import url
from lib.util import output
from lib.context import context
from lib.util import signal as sg
from lib.core import dispatcher

def init():
    initcolorama()
    initSignal()

def initSignal():
    signal.signal(signal.SIGINT, sg.ctrlC)
    signal.signal(signal.SIGTERM, sg.ctrlC)

def initArguments():
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="url to scan, eg: 'http://127.0.0.1/'")
    group.add_argument("--urls", type=argparse.FileType("r"), help="file contains urls to scan, one line one url.")

    parser.add_argument("--scale", default="full", help="build-in dictionary scale", choices=[i.split("/")[-1] for i in glob.glob("./dict/*")])
    # parser.add_argument("--folders", default=context.foldernames_dictionary, help="dictionary for most common folder names, default: {}".format(context.foldernames_dictionary))
    # parser.add_argument("--files", default=context.filenames_dictionary, help="dictionary for most common file names, default: {}".format(context.filenames_dictionary))
    # parser.add_argument("--backups", default=context.backups_dictionary, help="dictionary for most common backup file patterns, default: {}".format(context.backups_dictionary))
    parser.add_argument("--output", help="output folder, default: result/YYYY-MM-DD hh:mm:ss", default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    
    parser.add_argument("--threads", "-t", default=4, type=int, help="threads numbers, default: 4")
    parser.add_argument("--timeout", type=float, default=4, help="HTTP request timeout")

    parser.add_argument("--verbose", "-v", action="count", default=0, help="log level, eg: -v or -vv")
    parser.add_argument("--version", "-V", action="version", version="%(prog)s 2.0")

    args = parser.parse_args()
    return args

def main():
    init()

    # Parse command line arguments
    args = initArguments()

    # Parse urls
    urls = set()
    if args.url:
        urls = urls.union(url.Formater(args.url))
    if args.urls:
        for i in list(args.urls):
            x = url.Formater(i)
            urls = urls.union(x)

    # Start dispatching
    dispatcher.start(
        urls, 
        "dict/{}/{}".format(args.scale, context.foldernames_dictionary), 
        "dict/{}/{}".format(args.scale, context.filenames_dictionary), 
        "dict/{}/{}".format(args.scale, context.backups_dictionary), 
        args.threads,args.timeout
    )

    # Save result
    output.asCSV(args.output)

if __name__ == "__main__":
    main()
