#!/usr/bin/python
#coding: utf-8

import time
import datetime

def today2str():
    return '%s' % datetime.date.today()

def yesterday2str():
    return '%s' % (datetime.date.today() - datetime.timedelta(days=1))

def tomorrow2str():
    return '%s' % (datetime.date.today() + datetime.timedelta(days=1))

def timenow2str():
    """ Get now datetime str. """ 
    d = datetime.datetime.now()
    return d.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
    yesterday = yesterday2str()
    today = today2str()
    tomorrow = tomorrow2str()
    print yesterday, today, tomorrow
    print type(today)


