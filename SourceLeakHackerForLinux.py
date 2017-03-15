#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import requests
import ctypes
import sys


# config-start
timeout = 5
# config-end

class ColorPrinter:
    def print_red_text(self, content):
        print "\033[1;31;40m %s \033[0m" % (content),
    def print_green_text(self, content):
        print "\033[1;32;40m %s \033[0m" % (content),
    def print_blue_text(self, content):
        print "\033[1;34;40m %s \033[0m" % (content),


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
    if not colorPrinter :
        exit(1)
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
            response = requests.head(url,timeout = timeout)
            code = response.status_code
            if code == 200:
                colorPrinter.print_green_text("[ " + str(code) + " ]")
                print "Checking : " + url
                if "404" in response.text:
                    colorPrinter.print_blue_text(url + "\tMaybe every page same!")
            elif code == 404 or code == 405:
                pass
            else:
                colorPrinter.print_red_text("[ " + str(code) + " ]")
                print "Checking : " + url
        except Exception as e:
            print e


if __name__ == "__main__":
    main()
