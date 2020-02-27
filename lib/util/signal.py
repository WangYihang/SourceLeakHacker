import threading

from lib.context import context
from lib.util import output
from lib.util import logger

def ctrlC(signum, frame):
    logger.detail("CTRL C pressed, waiting for {} threads to exit...".format(threading.active_count()))
    context.CTRL_C_FLAG = True

