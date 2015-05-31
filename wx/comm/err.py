#!/usr/bin/python
# -*- coding:UTF-8

class ErrCode(object):
    SysErr = 1001
    ParamErr = 1002
    TypeErr = 1003
    ConfigErr = 1004
    ThirdErr = 2001
    APPErr = 3001
    WXApiErr = 4001

class IException(Exception):
    def __init__(self, code=0, info=''):
        self.code = code
        self.info = info

    def detail(self):
        err = "WXErr, code=%d,info=%s" % (self.code,  self.info)
        print err


if __name__ == '__main__':
    try:
        raise IException(1, 'xxxx') 
    except IException as IN:
        IN.detail()
    else:
        print "no exception"
        

