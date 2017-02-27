#!/usr/bin/env python
# encoding:utf-8

import threading
import sys

def check(url):
    try:
        response = requests.get(url,timeout = timeout)
        code = response.status_code
        if code == 200:
            colorPrinter.print_green_text("[ " + str(code) + " ]")
            print "Checking : " + url
            if "404" in response.text:
                colorPrinter.print_blue_text(url + "\tMaybe every page same!")
        else:
            colorPrinter.print_red_text("[ " + str(code) + " ]")
            print "Checking : " + url
    except Exception as e:
        print e


class myThread (threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self, url)
        self.url = url
def run(self):
    check(self.url)


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
    threads = []
    for i in listFile:
        i = i.replace("\n","")
        i = i.replace("\r","")
        if "?" in i:
            fileFile = open('file.txt', 'r')
            for j in fileFile:
                j = j.replace("\n","")
                j = j.replace("\r","")
                temp = i.replace("?",j)
                threads.append(myThread(website + temp))
        else:
            threads.append(myThread(website + i))

    for thread in threads:
        thread.start()
        while True:
            if (len(threading.enumrate() < threadNumber)):
                break

if __name__ == "__main__":
    main()
