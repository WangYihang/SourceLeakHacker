from termcolor import colored
from lib.util import color

def error(content):
    print(colored(content, 'red', 'on_grey'))

def correct(content):
    print(colored(content, 'green', 'on_grey'))

def detail(content):
    print(colored(content, 'blue', 'on_grey'))

def plain(content):
    print(colored(content, 'cyan', 'on_grey'))

def http(content, code):
    color_config = color.colorProjection(code)
    print(colored(content, color_config[0], color_config[1]))