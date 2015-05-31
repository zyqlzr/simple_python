#!/usr/bin/python
#coding: utf-8

import datetime
import json
import os
import time
import traceback
import urllib
import urllib2
import url_rsp

from api_const import WXCode
from api_const import WXErrInfo
from api_const import WXUrl
from err import IException
from err import ErrCode

#from py3rd import MultipartPostHandler
import singleton
import url_rsp

@singleton.singleton
class ApiTool(object):
    def __init__(self, appid, secretkey, timeout):
        self.__appid = appid
        self.__secretkey = secretkey
        self.__timeout = timeout
        self.access_token = None

    def __handle_rsp(self, respdict):
        if 'errcode' not in respdict:
            return True, WXCode.WX_OK, 'ok'
        if respdict['errcode'] == WXCode.WX_OK:
            return True, WXCode.WX_OK, 'ok'
        else:
            return False, respdict['errcode'], respdict['errmsg']

    def refresh_accesstoken(self):
        print 'ENTRANCE: appid:%s, secretkey:%s' % (self.__appid, self.__secretkey)
        try:
            url = WXUrl.ACCESS_TOKEN_URL % (self.__appid, self.__secretkey)
            headers = {'Content-Type':'application/json; encoding=utf-8'}
            resp = url_rsp.send_url_request(url=url, headers=headers)
            # save new access_token
            respdict = json.loads(resp)
            ret,code,info = self.__handle_rsp(respdict)
            if not ret:
                print 'get access failed,%d,%s' % (code,info)
                return False, code
            self.access_token = respdict['access_token']
        except Exception, e:
            print 'url exception while refresh'
            return False, WXCode.WX_ERR_EXCEPTION
        print 'refresh ok,new ACCESS_TOKEN:%s' % self.access_token
        return True, code

    def get_accesstoken(self):
        ret,code = self.refresh_accesstoken()
        if ret:
            return self.access_token
        else:
            return None

    def check_accesstoken(self):
        if self.access_token is None:
            return self.refresh_accesstoken()
        else:
            return True, WXCode.WX_OK

    def create_menu(self, button_list):
        ret, code = self.check_accesstoken()
        if not ret:
            return ret, code

        print 'ENTRANCE: button list:%s' % str(button_list)
        postdata = json.dumps(button_list, ensure_ascii=False).encode('utf-8')
        try:
            url = WXUrl.MENU_PUT_URL % self.access_token
            print 'menu url:%s' % url
            headers = {'Content-Type':'application/json; encoding=utf-8'}
            post = postdata

            resp = url_rsp.send_url_request(url=url, headers=headers, post=post)
            respdict = json.loads(resp)
            ret,code,info = self.__handle_rsp(respdict)
            if not ret:
                print 'handle response failed,code=%d,info=%s' % (code, info)
            return ret, code
        except Exception, e:
            print 'raise exception while get_menu'
            return False, WXCode.WX_ERR_EXCEPTION

    def create_menu_token(self, button_list, token):
        postdata = json.dumps(button_list, ensure_ascii=False).encode('utf-8')
        try:
            url = WXUrl.MENU_PUT_URL % token
            print 'menu url:%s' % url
            headers = {'Content-Type':'application/json; encoding=utf-8'}
            post = postdata

            resp = url_rsp.send_url_request(url=url, headers=headers, post=post)
            respdict = json.loads(resp)
            ret,code,info = self.__handle_rsp(respdict)
            if not ret:
                print 'handle response failed,code=%d,info=%s' % (code, info)
            return ret, code
        except Exception, e:
            print 'raise exception while get_menu'
            return False, WXCode.WX_ERR_EXCEPTION

    def get_menu(self):
        ret, code = self.check_accesstoken()
        if not ret:
            return None, code

        try:
            url = WXUrl.MENU_GET_URL % self.access_token
            headers = {'Content-Type':'application/json; encoding=utf-8'}

            resp = url_rsp.send_url_request(url=url, headers=headers)
            respdict = json.loads(resp)
            ret,code,info = self.__handle_rsp(respdict)
            if not ret:
                print 'handle response failed,code=%d,info=%s' % (code, info)
                return None, code
            return respdict, WXCode.WX_OK
        except Exception, e:
            print 'raise exception while get_menu'
            return None, WXCode.WX_ERR_EXCEPTION

    def get_menu_token(self, token):
        try:
            url = WXUrl.MENU_GET_URL % token
            headers = {'Content-Type':'application/json; encoding=utf-8'}

            resp = url_rsp.send_url_request(url=url, headers=headers)
            respdict = json.loads(resp)
            ret,code,info = self.__handle_rsp(respdict)
            if not ret:
                print 'handle response failed,code=%d,info=%s' % (code, info)
                return None, code
            return respdict, WXCode.WX_OK
        except Exception, e:
            print 'raise exception while get_menu'
            return None, WXCode.WX_ERR_EXCEPTION

    def delete_menu(self):
        ret, code = self.check_accesstoken()
        if not ret:
            return ret, code

        try:
            url = WXUrl.MENU_DEL_URL % self.access_token
            headers = {'Content-Type':'application/json; encoding=utf-8'}

            resp = url_rsp.send_url_request(url=url, headers=headers)
            respdict = json.loads(resp)
            ret,code,info = self.__handle_rsp(respdict)
            if not ret:
                print 'handle response failed,code=%d,info=%s' % (code, info)
            return ret, code
        except Exception, e:
            print 'raise exception while get_menu'
            return False, WXCode.WX_ERR_EXCEPTION

    def delete_menu_token(self, token):
        try:
            url = WXUrl.MENU_DEL_URL % token
            headers = {'Content-Type':'application/json; encoding=utf-8'}

            resp = url_rsp.send_url_request(url=url, headers=headers)
            respdict = json.loads(resp)
            ret,code,info = self.__handle_rsp(respdict)
            if not ret:
                print 'handle response failed,code=%d,info=%s' % (code, info)
            return ret, code
        except Exception, e:
            print 'raise exception while get_menu'
            return False, WXCode.WX_ERR_EXCEPTION


if __name__ == '__main__':
    print('api_const test')

