from termcolor import colored

def colorProjection(code):
    if (code / 100) == 1:
        return ("blue", "on_grey")
    elif (code / 100) == 2:
        return ("green", "on_grey")
    elif (code / 100) == 3:
        return ("yellow", "on_grey")
    elif (code / 100) == 4:
        return ("red", "on_grey")
    elif (code / 100) == 5:
        return ("magenta", "on_grey")
    else:
        return ("cyan", "on_grey")

def colorByStatusCode(data, code):
    color_config = colorProjection(code)
    return colored(data, color_config[0], color_config[1])
