#!/usr/bin/env python
# encoding:utf-8

import threading
import requests
import signal
import sys
import glob
import time
import argparse
import prettytable
import coloredlogs
import os
import logging

from lib.util import url
from lib.util import output
from lib.context import context
from lib.util import signal as sg
from lib.core import dispatcher

def init():
    initSignal()

def initSignal():
    signal.signal(signal.SIGINT, sg.ctrlC)
    signal.signal(signal.SIGTERM, sg.ctrlC)

def initArguments():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [options]", 
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="A multi threads web application source leak scanner", 
        epilog='''
Examples: 
    1. For a single url('http://baidu.com') to scan: 
        ```
        python SourceLeakHacker.py --url=http://baidu.com --scale=tiny --threads=4 --timeout=8 
        ```
    2. For a bunch of urls in file('url.txt') to scan: 
        ```
        python SourceLeakHacker.py --urls=url.txt --threads=4 --timeout=8 --level=INFO 
        ```
        '''
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", "-u", help="url to scan, eg: 'http://127.0.0.1/'")
    group.add_argument("--urls", type=argparse.FileType("r"), help="file contains urls to scan, one line one url.")

    parser.add_argument("--scale", "-s", default="full", help="build-in dictionary scale", choices=[i.split(os.sep)[-1] for i in glob.glob("./dict/*")])
    # parser.add_argument("--folders", default=context.foldernames_dictionary, help="dictionary for most common folder names, default: {}".format(context.foldernames_dictionary))
    # parser.add_argument("--files", default=context.filenames_dictionary, help="dictionary for most common file names, default: {}".format(context.filenames_dictionary))
    # parser.add_argument("--backups", default=context.backups_dictionary, help="dictionary for most common backup file patterns, default: {}".format(context.backups_dictionary))
    parser.add_argument("--output", "-o", help="output folder, default: result/YYYY-MM-DD-hh-mm-ss", default=time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())))

    parser.add_argument("--threads", "-t", default=4, type=int, help="threads numbers, default: 4")
    parser.add_argument("--timeout", type=float, default=4, help="HTTP request timeout")

    levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG",]
    parser.add_argument("--level", "-v", choices=levels, default="WARNING", help="log level")
    parser.add_argument("--version", "-V", action="version", version="%(prog)s 3.0")

    args = parser.parse_args()
    return args

def save_dictionary(filename, dictionary):
    with open(filename, "w") as f:
        for k, v in dictionary.items():
            f.write("{}-{}\n".format(v, k))

def main():
    init()
    # Parse command line arguments
    args = initArguments()

    # Logger
    logger = logging.getLogger(__name__)
    coloredlogs.install(
        level=args.level, 
        fmt='%(asctime)s [%(levelname)s] %(message)s'
    )
    context.logger = logger

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

    # Save optimized dictionary
    context.logger.info("Saving optimized dictionary: dict/{}/{}".format(args.scale, context.foldernames_dictionary))
    save_dictionary("dict/{}/{}".format(args.scale, context.foldernames_dictionary), context.foldernames_cache)
    context.logger.info("Saving optimized dictionary: dict/{}/{}".format(args.scale, context.filenames_dictionary))
    save_dictionary("dict/{}/{}".format(args.scale, context.filenames_dictionary), context.filenames_cache)
    context.logger.info("Saving optimized dictionary: dict/{}/{}".format(args.scale, context.backups_dictionary))
    save_dictionary("dict/{}/{}".format(args.scale, context.backups_dictionary), context.backups_cache)

    # Print statistic information
    output.asTable()

    # Save result
    output.asCSV(args.output)

if __name__ == "__main__":
    main()
