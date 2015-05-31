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
import menu_mgn
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

HELP = '''
    [1] menu update
    [2] menu remove
    [-1] Bye!
'''

class MenuTool(object):
    def __init__(self, conf_path):
        self.conf = Config()
        self.conf.load(conf_path)
        self.mongo = wx_mongo.WxMongo()
        self.mongo.start()

    def process_input(self, param):
        param_num = len(param)
        if 0 == param_num:
            print 'param num is 0, check it\n', HELP
            return
        if param[0] == 'menu':
            self.process_menu(param, param_num)
        else:
            print HELP

    def process_menu(self, param, param_num):
        if param_num < 3:
            print 'parameter number is too less\n', HELP
            return 
        cmd = param[1]
        cmd3 = param[2]
        print 'input last=',cmd3
        if cmd == 'update':
            self.process_menu_update(cmd3)
        elif cmd == 'remove':
            self.process_menu_remove(cmd3)
        else:
            print HELP

    def process_menu_update(self, cmd):
        mmgn = menu_mgn.MenuMgn()
        mmgn.load(cmd)
        mmgn.update()

    def process_menu_remove(self, cmd):
        mmgn = menu_mgn.MenuMgn()
        mmgn.load(cmd)
        mmgn.remove_menu()

    def loop(self):
        while True:
            input = raw_input()
            param = input.split(' ')
            #try:
            self.process_input(param)
            #except IException:
            #    print HELP

if __name__ == '__main__':
    conf_path = './wm.xml'
    tool = MenuTool(conf_path)
    tool.loop() 

