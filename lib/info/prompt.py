from lib.util import logger

def show(name):
    logger.plain("Usage : ")
    logger.plain("        python %s [URL] [ThreadNumbers] [Timeout]" % (name))
    logger.plain("Example : ")
    logger.plain("        python %s http://127.0.0.1/ 2 5" % (name))
    logger.plain("Tips : ")
    logger.plain("        2 - 3 threadNumber is recommended.")
    logger.plain("        5 second timeout is recommended.(You can also use a decimal to set the timeout.)")
    logger.plain("        If you have any questions, please contact <wangyihanger@gmail.com>")
