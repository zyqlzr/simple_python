#!/usr/bin/python
# -*- coding=utf-8 -*-

import time
import json
import pymongo
import config
import wx_mongo
import order_notify

from comm import mytime
from comm.err import IException
from comm import err
from wx_mongo import WxMongo
import menu_mgn
import html_mgn

def menu_test(): 
    conf = config.Config()
    conf.load('./unit/test.xml')
    print conf.to_string()
    mongo = wx_mongo.WxMongo()
    mongo.start()

    mmgn = menu_mgn.MenuMgn()
    mmgn.load('./menu.xml')
    mmgn.update()

    hmgn = html_mgn.html_mgn()
    html = hmgn.get_week_now()
    print html.encode('utf-8')

def menu_del():
    conf = config.Config()
    conf.load('./unit/test.xml')
    print conf.to_string()
    mongo = wx_mongo.WxMongo()
    mongo.start()

    mmgn = menu_mgn.MenuMgn()
    mmgn.load('./test_m.xml')
    mmgn.remove_menu()

