#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
import os
import sys
import time
import traceback

import tornado.ioloop
import tornado.options
import tornado.web

from comm.err import IException
from comm.mylogger import MyLogger as LOG 
from wx_server import WxServer as SVR
from config import Config as CONF
import wx_xml

class SimepleHandler(tornado.web.RequestHandler):
    def get(self):
        print 'recv http get'
        self.write('get ok')

    def post(self):
        print 'recv http post'
        self.write('post ok')

class MenuHandler(tornado.web.RequestHandler):
    svr = SVR()
    conf = CONF()

    def get_current_user(self):
        return self.get_secure_cookie('user')

    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            # in debug mode, try to send a traceback
            if self.settings.get('debug'):
                for line in traceback.format_exception(*kwargs['exc_info']):
                    self.write(line + '<br />')
            self.finish()
        else:
            self.finish('Bad guy!!!!')

    def get(self):
        self._debug() 
        if ('signature' not in self.request.arguments or
           'timestamp' not in self.request.arguments or
           'nonce' not in self.request.arguments or
           'echostr' not in self.request.arguments):
            return
        # check signature
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')

        check_ok = self.svr.check_signature(signature, timestamp, nonce, self.conf.token)
        if not check_ok:
            print 'check signature failed'
            return

        print 'check signature ok'
        self.write(echostr)

    def post(self):
        try:
            self._debug()
            reply = self.svr.do_request(self.request.arguments, self.request.body)
            if reply is None:
                print 'reply is none'
                return ''
            #print reply.encode('utf-8')
            self.write(reply)
        except IException as e:
            e.detail()
        #except Exception as base_e:
        #    print 'wx exception'
        #    print(base_e)
            #traceback.print_stack()
       #     return

    def _debug(self):
        print 'request_method=%s' % self.request.method
        print 'request_url=%s' % self.request.uri
        print 'request_headers=%s' % self.request.headers
	print 'request_body=%s' % self.request.body
        print 'request_arguments=%s' % self.request.arguments
