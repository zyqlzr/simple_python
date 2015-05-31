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

import comm.url_rsp
import comm.api_const
import config
import html_const
import order_mgn

class OrderHandler(tornado.web.RequestHandler):
    om = order_mgn.OrderMgn()
    conf = config.Config()
    def get(self):
        if 'code' in self.request.arguments:
            code_val = self.get_argument('code')
            access_url = comm.api_const.WXUrl.ACCESS_URL % (self.conf.appid, self.conf.appsecret, code_val)
            print 'code_val:', code_val
            access_val = comm.url_rsp.send_url_request(access_url)
            print access_val
            html = self.om.get_order_html(access_val)
            #print 'return order html to user:\n', html.encode('utf-8')
            self.write(html)
        else:
            self.write('can not find code')

    def post(self):
        self._debug()
        if 'submit' in self.request.arguments:
            id = self.get_argument('submit')
            print 'submit id=',id
        order_info = json.loads(self.request.body)
        print order_info
        self.om.process_order(order_info)
        ret = json.dumps({'ok': 200})
        self.write(ret)

    def _debug(self):
        print 'request=',self.request
        print 'request_body=', self.request.body


class ShoppingHandler(tornado.web.RequestHandler):
    om = order_mgn.OrderMgn()
    conf = config.Config()
    def get(self):
        if 'code' in self.request.arguments:
            code_val = self.get_argument('code')
            access_url = comm.api_const.WXUrl.ACCESS_URL % (self.conf.appid, self.conf.appsecret, code_val)
            access_val = comm.url_rsp.send_url_request(access_url)
            html = self.om.get_order_history_html(access_val)
            print html
            self.write(html)
        else:
            self.write('can not find code')

    def post(self):
        return

