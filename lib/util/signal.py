import threading

from lib.context import context
from lib.util import output

def ctrlC(signum, frame):
    context.logger.warning("CTRL C pressed, waiting for {} threads to exit...".format(threading.active_count()))
    context.CTRL_C_FLAG = True
