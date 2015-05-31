#!/usr/bin/python
# -*- coding=utf-8 -*-

from comm import api_tool
from comm import api_const
from config import Config 
from comm.mylogger import MyLogger as LOG
from comm.err import IException
from comm.err import ErrCode
import wx_menu
import wx_mongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

HELP = '''
    [1] menu create
    [2] menu get
    [3] menu del
    [-1] Bye!
'''

class Tool(object):
    def __init__(self, log_path, conf_path):
        LOG().setlogger(log_path)
        self.conf = Config()
        self.conf.load(conf_path)
        self.app_id = self.conf.appid
        self.app_secret = self.conf.appsecret
        self.mongo = wx_mongo.WxMongo()
        self.mongo.start()

        print 'app_id=%s,key=%s' % (self.app_id, self.app_secret)
        self.tool = api_tool.ApiTool(self.conf.appid, 
            self.conf.appsecret, 3000)


    def process(self, param):
        param_num = len(param)
        if 0 == param_num:
            print 'param num is 0',HELP
            return
        if param[0] == 'menu':
            self.process_menu(param, param_num)
        else:
            print 'un-recognition',HELP

    def process_menu(self, param, param_num):
        if param_num < 2:
            print 'parameter is too smaller',HELP
            return
        cmd = param[1]
        token_cache = self.mongo.cache.get_key('access_token')
        token = token_cache['value']
        print token
        if cmd == 'create':
            print token
            ret, ccode = self.tool.create_menu_token(wx_menu.wx_curr_menu, token)
            if not ret:
                print 'create menu err,info=%s' % api_const.WXErrInfo[ccode]
            else:
                print 'create menu ok'
        elif cmd == 'get':
            rsp, gcode = self.tool.get_menu_token(token)
            if rsp is None:
                print 'get menu err,info=%s' % api_const.WXErrInfo[gcode]
            else:
                print 'get menu ok,menu=%s' % str(rsp)
        elif cmd == 'del':
            ret, code = self.tool.delete_menu_token(token)
            if not ret:
                print 'delete menu err,info=%s' % api_const.WXErrInfo[code]
            else:
                print 'delete menu ok'
        else:
            print HELP
            return

    def loop(self):
        while True:
            input = raw_input()
            param = input.split(' ');
            self.process(param)

if __name__ == '__main__':
    log_path = './log'
    conf_path = './wm.xml'
    tool = Tool(log_path, conf_path)
    tool.loop() 
