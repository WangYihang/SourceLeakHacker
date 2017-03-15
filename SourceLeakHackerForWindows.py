#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import requests
import winsound # 在 windows 平台可以通过提示音来提示
import ctypes
import sys


# config-start
timeout = 5
# config-end


STD_INPUT_HANDLE = -10  
STD_OUTPUT_HANDLE= -11  
STD_ERROR_HANDLE = -12  

FOREGROUND_BLACK = 0x0  
FOREGROUND_BLUE = 0x01 # text color contains blue.  
FOREGROUND_GREEN= 0x02 # text color contains green.  
FOREGROUND_RED = 0x04 # text color contains red.  
FOREGROUND_INTENSITY = 0x08 # text color is intensified.  

BACKGROUND_BLUE = 0x10 # background color contains blue.  
BACKGROUND_GREEN= 0x20 # background color contains green.  
BACKGROUND_RED = 0x40 # background color contains red.  
BACKGROUND_INTENSITY = 0x80 # background color is intensified.  

class ColorPrinter:  
    ''''' See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp 
    for information on Windows APIs.'''  
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)  

    def set_cmd_color(self, color, handle=std_out_handle):  
        """(color) -> bit 
        Example: set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY) 
        """  
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)  
        return bool  

    def reset_color(self):  
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)  

    def print_red_text(self, print_text):  
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)  
        print print_text  
        self.reset_color()  

    def print_green_text(self, print_text):  
        self.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)  
        print print_text  
        self.reset_color()  

    def print_blue_text(self, print_text):   
        self.set_cmd_color(FOREGROUND_BLUE | FOREGROUND_INTENSITY)  
        print print_text  
        self.reset_color()  

    def print_red_text_with_blue_bg(self, print_text):  
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY| BACKGROUND_BLUE | BACKGROUND_INTENSITY)  
        print print_text  
        self.reset_color()     

def urlFormater(url):
    if (not url.startswith("http://")) and (not url.startswith("https://")):
        url = "http://" + url
    if not url.endswith("/"):
        url += "/"
    return url

def main():
    if len(sys.argv) != 2:
        print "Usage : "
        print "        python %s [URL]" % (sys.argv[0])
        print "Example : "
        print "        python %s http://www.baidu.com/" % (sys.argv[0])
        print "Tips : "
        print "        Your URL should must starts with \"http://\" or \"https://\""
        print "        If you have any questions, please contact [ wangyihanger@gmail.com ]"
        exit(1)

    website = urlFormater(sys.argv[1])
    colorPrinter = ColorPrinter()
    listFile = open('list.txt', 'r')
    urls = []
    for i in listFile:
        i = i.replace("\n","")
        i = i.replace("\r","")
        if "?" in i:
            fileFile = open('file.txt', 'r')
            for j in fileFile:
                j = j.replace("\n","")
                j = j.replace("\r","")
                temp = i.replace("?",j)
                urls.append(website + temp)
        else:
            urls.append(website + i)

    for url in urls:
        try:
            print "Checking :", url,
            response = requests.head(url,timeout = timeout)
            code = response.status_code
            if code == 200:
                colorPrinter.print_green_text("[ " + str(code) + " ]")
                winsound.Beep(1000,1000)
                if "404" in response.text:
                    colorPrinter.print_blue_text(url + "\tMaybe every page same!")
            elif code == 404 or code == 405:
                pass
            else:
                colorPrinter.print_red_text("[ " + str(code) + " ]")
        except Exception as e:
            print e


if __name__ == "__main__":
    main()
