import requests
import threading
import time

from lib.context import context
from lib.util import logger
from lib.util import color

# Different path may has different server
# This function is able to sniff the server info
def sniff(url, timeout):
    # TODO
    pass

def check(url, timeout):
    try:
        if timeout <= 0:
            timeout = 4
            
        start_time = time.time()
        response = requests.head(url, timeout = timeout)
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
        pass

class Spider(threading.Thread):
    def __init__(self, url, timeout):
        threading.Thread.__init__(self)
        self.url = url
        self.timeout = timeout

    def run(self):
        check(self.url, self.timeout)
