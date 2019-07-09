import subprocess
import platform
import sys

def clear():
    if platform.system()=="Windows":
        subprocess.Popen("cls", shell=True).communicate()
    else:
        sys.stdout.write("\033c")