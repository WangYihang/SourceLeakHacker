
from lib.context import context
from lib.util import output
from lib.util import logger

def ctrlC(signum, frame):
    logger.detail("CTRL C pressed, exiting...")
    context.CTRL_C_FLAG = True

