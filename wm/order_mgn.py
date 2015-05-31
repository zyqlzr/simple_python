#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
import os
import sys
import time
import datetime
import traceback

import comm.mytime
from comm import singleton
from comm.err import ErrCode
from comm.err import IException
from comm.mylogger import MyLogger as LOG 
import config
import wx_mongo
import html_generator
import order_notify
import discount_mgn

@singleton.singleton
class OrderMgn(object):
    def init(self):
        self.log = LOG().getlogger()
        self.mongo = wx_mongo.WxMongo()
        self.counter = order_notify.OrderCounter()
        self.dm = discount_mgn.DiscountMgn() 

    def parse(self, access_ret=None):
        decode = json.loads(access_ret)
        try:
            openid = decode['openid']
        except KeyError:
            return None
        return openid

    def get_order_info(self, openid=None):
        if openid is None:
            raise IException(ErrCode.ParamErr, 'access is null')
        arrs = []
        history = self.mongo.shopping.get_shopping(openid)
        if history is None or 'history' not in history:
            return arrs
        #print '****history*****:',history
        arrs = history['history']
        arrs_len = len(arrs)
        if arrs_len > 10:
            arrs_begin = arrs_len - 10
            arrs = arrs[arrs_begin : arrs_len]
        arrs = arrs[::-1]
        result = []
        for ele in arrs:
            order_ele = self.mongo.order.get_order(ele)
            #print '***(k,v)***:',ele,order_ele
            result.append(order_ele)
        return result

    def get_order_history_html(self, access_ret=None):
        if access_ret is None:
            raise IException(ErrCode.ParamErr, 'access is null')
        openid = self.parse(access_ret) 
        if openid is None:
            return False, None
        arr = self.get_order_info(openid)
        #print '***order_list***:',arr
        hg = html_generator.HtmlGenerator()
        return hg.generate_order_page(arr)

    def get_user_info(self, openid=None):
        if openid is None:
            raise IException(ErrCode.ParamErr, 'access is null')
        info = self.mongo.user.find_last_info(openid)
        if info is None:
            self.mongo.user.subscribe(openid)
        return info 

    def get_order_html(self, access_ret=None):
        if access_ret is None:
            raise IException(ErrCode.ParamErr, 'access is null')
        openid = self.parse(access_ret) 
        if openid is None:
            return False, None

        info = self.get_user_info(openid)
        dc_info = self.dm.discount(openid)
        hg = html_generator.HtmlGenerator()
        return hg.generate_page(openid, info, dc_info)

    def get_shopping_html(self, access_ret=None):
        if access_ret is None:
            raise IException(ErrCode.ParamErr, 'access is null')
        openid = self.parse(access_ret) 
        if openid is None:
            return False, None

    def process_order(self, order_info={}):
        if len(order_info) == 0:
            raise IException(ErrCode.ParamErr, 'order is empty')
        if 'id' not in order_info or 'menu' not in order_info:
            raise IException(ErrCode.ParamErr, 'order lack')

        openid = order_info['id']
        omenu = order_info['menu']
        oprice = order_info['price']
        odc = order_info['discount']
        print 'price type:', type(oprice),',discount type:',odc,',discount:',odc
        oaddr = None
        if 'user_info' in order_info:
            info = order_info['user_info']
            ret, oaddr = self.order_add_addr(openid, info)
        else:
            ret, oaddr = self.order_mongo_addr(openid)
        self.order_save_notify(openid, oaddr[0], oaddr[1], omenu, oprice, odc)
        if odc > 0:
            self.dm.discount_first_check(openid)

    def order_save_notify(self, oid=None, oaddr=None, 
            ophone=None, omenu={}, oprice=None, odc=0):
        if (oid is None or oaddr is None or ophone is None 
                or oprice is None):
            raise IException(ErrCode.ParamErr, 'input null')
        ocount = self.counter.cas_counter()
        self.order_save(oid, ocount, oprice, omenu, odc)
        order_notify.OrderNotify().notify(ocount, oaddr, ophone, omenu, oprice, odc)

    def order_save(self, oid, ocount, oprice, omenu, odc):
        odtime = comm.mytime.today2str()
        omenu_val = []
        for key in omenu:
            i = omenu[key]
            tmp = {}
            tmp['m'] = key
            if 'num' in i:
                tmp['n'] = i['num']
            if 'title' in i:
                tmp['t'] = i['title']
            omenu_val.append(tmp)

        #print omenu_val
        order_key = odtime + ':' + str(ocount)
        self.mongo.order.add_order(id=oid, order_id=order_key, menu=omenu_val, price=oprice, discount=odc)
        self.mongo.shopping.add_shopping(id=oid, order_id=order_key)
        self.mongo.stat.order(odtime, order_id=order_key)

    def order_add_addr(self, openid=None, order_info=None):
        if openid is None or order_info is None:
            raise IException(ErrCode.ParamErr, 'input null')
        try:
            o_type = order_info['type']
            o_addr = order_info['addr']
            o_phone = order_info['phone']
        except KeyError:
            raise IException(ErrCode.ThirdErr, 'set-find error')
        if o_type == 0 or o_type == 1:
            self.mongo.user.update(openid, 0, o_phone, o_addr)
        return True, (o_addr, o_phone)

    def order_mongo_addr(self, openid=None):
        info = self.get_user_info(openid)
        if info is None or 'lastest_info' not in info:
            return False, None
        last_info = info['lastest_info']
        if 'addr' not in last_info or 'phone' not in last_info:
            return False, None
        return True, (last_info['addr'], last_info['phone'])


