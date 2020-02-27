import prettytable
import csv
import os

from lib.util import string
from lib.util import color
from lib.context import context

headers = ["Code", "Length", "Time", "Type", "URL"]

def asTable():
    # table = prettytable.PrettyTable()
    # table.field_names = headers
    # for k, v in context.result.items():
    #     if v["code"] != 404:
    #         table.add_row([
    #             color.colorByStatusCode(v["code"], v["code"]), 
    #             # v["code"],
    #             v["Content-Length"], 
    #             "%02f" % v["time"], 
    #             v["Content-Type"], 
    #             # string.fixLength(k, 0x20)
    #             k,
    #         ])
    # table.set_style(prettytable.MSWORD_FRIENDLY)
    # print(table)
    table = prettytable.PrettyTable()
    table.field_names = ["Code", "Times"]
    for k, v in context.statistic.items():
        table.add_row([k, v])
    print(table)

def asCSV(foldername):
    folder = "result/{}".format(foldername)
    # Create folder
    try:
        os.mkdir(folder)
    except OSError:
        print ("Creation of the directory %s failed" % folder)

    codes = context.statistic.keys()
    writers = {}

    for code in codes:
        filename = "{}/{}.csv".format(folder, code)
        context.logger.info("Saving result into file: {}".format(filename))
        f = open(filename, "w")
        cvs_writer = csv.writer(f)
        cvs_writer.writerow(headers)
        writers[code] = cvs_writer

    for k, v in context.result.items():
        writers[v["code"]].writerow([v["code"], v["Content-Length"], v["time"], v["Content-Type"], k])
    context.logger.info("Result saved in files: {}/{}.csv".format(folder, list(writers.keys())))