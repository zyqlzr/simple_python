#!/usr/bin/python
# -*- coding=utf-8 -*-

import os
# Change path to current file path
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import tornado.ioloop
import tornado.options
import tornado.web

from config import Config
from html_mgn import html_mgn

from comm.mylogger import MyLogger as LOG
from wm_handler import WMHandler
from wm_handler import TestHandler
from order_handler import OrderHandler
from order_handler import ShoppingHandler 

import order_mgn
import order_notify
import discount_mgn
import wx_mongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

tornado.options.define('port', default=8000, help='run on the given port', type=int)

def main():
    settings = {
        'cookie_secret': '66oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
        'login_url':  r'/login',
        'debug': True,
    }

    #load config xml and init logger
    conf = Config()
    conf.load('./wm.xml')
    LOG().setlogger('./wm.log')
    print conf.to_string()

    html_mgn().start(conf.bnum)
    wx_mongo.WxMongo().start()

    omgn = order_mgn.OrderMgn()
    omgn.init()
    onotify = order_notify.OrderNotify()
    onotify.start(wx_mongo.WxMongo(), conf)
    discount_mgn.DiscountMgn().start('./dc.xml')
    print 'server ip[%s],port[%d]' % (conf.ip, conf.port)
    # Start server
    app = tornado.web.Application([
        (r'/wm', WMHandler),
        (r'/openid', OrderHandler),
        (r'/shopping', ShoppingHandler),
        (r'/test', TestHandler),
        ], **settings)

    app.listen(conf.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

