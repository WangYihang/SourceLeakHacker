import prettytable
import csv

from lib.util import string
from lib.util import color
from lib.context import context

headers = ["Code", "Length", "Time", "Type", "URL"]

def asTable():
    table = prettytable.PrettyTable()
    table.field_names = headers
    for k, v in context.result.items():
        if v["code"] != 404:
            table.add_row([
                # color.colorByStatusCode(v["code"], v["code"]), 
                v["code"],
                v["headers"]["Content-Length"], 
                v["time"], 
                v["headers"]["Content-Type"], 
                string.fixLength(k, 0x20)]
            )
    table.set_style(prettytable.MSWORD_FRIENDLY)
    print(table)

def asCSV(filename):
    with open(filename, 'w') as f:
        cvs_writer = csv.writer(f)
        cvs_writer.writerow(headers)
        for k, v in context.result.items():
            cvs_writer.writerow([v["code"], v["headers"]["Content-Length"], v["time"], v["headers"]["Content-Type"], k])