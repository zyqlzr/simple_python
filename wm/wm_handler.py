#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
import os
import sys
import time
import datetime
import traceback

import tornado.ioloop
import tornado.options
import tornado.web

from comm.err import IException
from comm.mylogger import MyLogger as LOG 
import comm.mytime
import config
import html_mgn

class WMHandler(tornado.web.RequestHandler):
    conf = config.Config()
    html = html_mgn.html_mgn()

    def get(self):
        self._debug() 

        if 'menu' in self.request.arguments:
            menu_day = self.get_argument('menu')
            if menu_day == 'week':
                #html_data = self.html.today_menu()
                hour = comm.mytime.hournow()
                print hour
                if  hour < 5 or hour >= 24:
                    html_data = self.html.get_week_timeout()
                else:
                    html_data = self.html.get_week_now()
                self.write(html_data)
            else:
                self.write('menu command is invalid')
        elif 'time' in self.request.arguments:
            menu_day = self.get_argument('time')
            if menu_day == 'week':
                html_data = self.html.get_week_time()
                self.write(html_data)
            else:
                self.write('menu command is invalid')
        else:
            ret = 'arguments in request is invalid'
            self.write(ret)

    def post(self):
        return

    def _debug(self):
        print 'request',self.request

class TestHandler(tornado.web.RequestHandler):
    conf = config.Config()
    html = html_mgn.html_mgn()
    def get(self):
        self._debug() 
        if 'week' in self.request.arguments:
            week_day = self.get_argument('week')
            print 'week_day=', week_day
            html_data = self.html.get_week_test(week_day)
            print html_data.encode('utf-8')
            self.write(html_data)
        else:
            self.write('menu command is invalid')

    def post(self):
        return

    def _debug(self):
        print 'request',self.request

