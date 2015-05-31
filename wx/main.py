#!/usr/bin/python
# -*- coding=utf-8 -*-


import os
# Change path to current file path
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import tornado.ioloop
import tornado.options
import tornado.web

from wx_server import WxServer
from config import Config
from menu_handler import MenuHandler
from menu_handler import SimepleHandler 
from comm.mylogger import MyLogger as LOG

import url_mgr
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

    app = tornado.web.Application([
        (r'/main', MenuHandler),
        ], **settings)

    #print config.CGI_BIN_ACCESS_PATH_PREFIX + r'/interface/main'

    # Init logger
    LOG().setlogger('./wx.log')
    url_mgr.UrlMgr().init('./url.xml', LOG().getlogger())
    WxServer().start('./wx.xml')
    print 'server ip[%s],port[%d]' % (Config().ip, Config().port)
    # Start server
    app.listen(Config().port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()


