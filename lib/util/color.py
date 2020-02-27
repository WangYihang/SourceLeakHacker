from colorama import Fore

def projection(code):
    if int(code / 100) == 1:
        return Fore.BLUE
    elif int(code / 100) == 2:
        return Fore.GREEN
    elif int(code / 100) == 3:
        return Fore.YELLOW
    elif int(code / 100) == 4:
        return Fore.RED
    elif int(code / 100) == 5:
        return Fore.MAGENTA
    else:
        return Fore.CYAN
