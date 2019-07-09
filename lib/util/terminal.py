import subprocess
import platform

def clear():
    if platform.system()=="Windows":
        subprocess.Popen("cls", shell=True).communicate()
    else:
        print("\033c", end="")