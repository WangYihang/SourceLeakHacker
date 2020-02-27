from termcolor import colored
from lib.util import color
from lib.context import context

def error(content):
    context.screenLock.acquire()
    print(colored(content, "red", "on_grey"))
    context.screenLock.release()

def correct(content):
    context.screenLock.acquire()
    print(colored(content, "green", "on_grey"))
    context.screenLock.release()

def detail(content):
    context.screenLock.acquire()
    print(colored(content, "blue", "on_grey"))
    context.screenLock.release()

def plain(content):
    context.screenLock.acquire()
    print(colored(content, "white", "on_grey"))
    context.screenLock.release()

def http(content, code):
    context.screenLock.acquire()
    color_config = color.colorProjection(code)
    print(colored(content, color_config[0], color_config[1]))
    context.screenLock.release()
