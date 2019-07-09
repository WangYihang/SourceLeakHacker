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
        context.screenLock.acquire()

        if timeout <= 0:
            timeout = 4
        start_time = time.time()
        response = requests.head(url, timeout = timeout)
        end_time = time.time()

        code = response.status_code
        content_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        time_used = end_time - start_time

        context.result[url] = {
            "code":code,
            "headers":response.headers,
            "time":time_used,
        }

        if (code / 100) == 1:
            logger.http("[%d]\t%d\t%02f\t%s\t%s" % (code, content_length, time_used, content_type, url), code)
        elif (code / 100) == 2:
            logger.http("[%d]\t%d\t%02f\t%s\t%s" % (code, content_length, time_used, content_type, url), code)
            # Some site use one response for pages not exists.
            # Try to avoid that situation
            if "404" in response.text:
                logger.error(url + "\tMaybe every page same!")
        elif (code / 100) == 3:
            logger.http("[%d]\t%d\t%02f\t%s\t%s" % (code, content_length, time_used, content_type, url), code)
        elif (code / 100) == 4:
            logger.http("[%d]\t%d\t%02f\t%s\t%s" % (code, content_length, time_used, content_type, url), code)
        elif (code / 100) == 5:
            logger.http("[%d]\t%d\t%02f\t%s\t%s" % (code, content_length, time_used, content_type, url), code)
        else:
            logger.error("[%d]\t%d\t%02f\t%s\t%s" % (code, content_length, time_used, content_type, url))
    except Exception as e:
        context.screenLock.acquire()
        logger.error(e)
    finally:
        pass
        context.screenLock.release()

class Spider(threading.Thread):
    def __init__(self, url, timeout):
        threading.Thread.__init__(self)
        self.url = url
        self.timeout = timeout

    def run(self):
        check(self.url, self.timeout)
