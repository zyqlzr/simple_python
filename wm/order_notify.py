#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
import threading
import time

import comm.api_tool
import comm.mytime
from comm import singleton
from comm.err import ErrCode
from comm.err import IException
import comm.url_rsp
import comm.api_const
import order_format
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

WX_CACHE_TOKEN = 'access_token'

@singleton.singleton
class OrderCounter(object):
    def __init__(self):
        self.counter = 0
        self.lock = threading.Lock()

    def cas_counter(self):
        self.lock.acquire() 
        counter = self.counter + 1
        self.counter = counter
        self.lock.release()
        return counter

    def set_counter(self, num):
        self.lock.acquire()
        self.counter = num
        self.lock.release()
        return self.counter

    def reset_counter(self):
        self.lock.acquire()
        self.counter = 0
        self.lock.release()


class TokenRefresher(threading.Thread):
    def start_refresh(self, mongo, conf):
        self.mongo = mongo
        self.flag = True
        self.tool = comm.api_tool.ApiTool(conf.appid, conf.appsecret, 3000)
        self.tt = conf.token_tt 
        self.tg = conf.token_tg
        self.start()
        self.day = comm.mytime.today2str()

    def stop_refresh(self):
        self.flag = False

    def run(self):
        print 'end run'
        last_ts = None
        while self.flag:
            ts = int(time.time())
            if last_ts is None or (ts - last_ts) > self.tg:
                last_ts = ts
                if last_ts is None:
                    print 'ts=%d' % ts
                else:
                    print 'last_ts=%d,ts=%d' % (last_ts, ts)
                self.refresh_token()
            self.day_change()
            time.sleep(self.tt)
            print 'one loop'

    def refresh_token(self):
        token = self.tool.get_accesstoken()
        if token is None:
            print 'get access token failed'
            return

        #cache_a = self.mongo.cache.get_key(WX_CACHE_TOKEN)
        self.mongo.cache.set_key(WX_CACHE_TOKEN, token)
        #cache_b = self.mongo.cache.get_key(WX_CACHE_TOKEN)
        print '*refresh*,token=%s' % token
        #if cache_a is not None and cache_b is not None:
        #    print 'token cache a=%s,b=%s' % (cache_a, cache_b)

    def day_change(self):
        today = comm.mytime.today2str()
        if today != self.day:
            OrderCounter().reset_counter()
            self.day = today

@singleton.singleton
class OrderNotify(object):
    def start(self, mongo, conf):
        self.mongo = mongo
        self.conf = conf
        self.refresher = TokenRefresher()
        self.refresher.setDaemon(True)
        self.refresher.start_refresh(self.mongo, self.conf)
        self.customers = self.conf.customers
        self.get_old_counter()

    def stop(self):
        self.refresher.stop_refresh()

    def get_old_counter(self):
        day = comm.mytime.today2str()
        arr = self.mongo.stat.find_order(day)
        arr_len = len(arr)
        if 0 == arr_len:
            return
        counter = 0
        for i in arr:
            vals = i.split(':')
            if len(vals) != 2:
                print 'order id invalid'
                continue
            tmp_count = int(vals[1])
            print 'tmp counter:', tmp_count
            if tmp_count > counter:
                counter = tmp_count
        gc = OrderCounter().set_counter(counter)
        print 'order counter value=',gc

    def notify(self, count, addr, phone, menu, price, dc):
        print 'order notify:',menu
        notify_info = order_format.ORDER_FORMAT % (count, 
            addr, phone, price, dc, self.menu2str(menu))
        self.send_to_admin(notify_info)

    def menu2str(self, menu):
        menu_str = ''
        for key in menu:
           i_menu = menu[key]
           if 'num' in i_menu and 'title' in i_menu:
               i_str = order_format.MENU_FORMAT % (i_menu['title'], i_menu['num'])
               menu_str += i_str
        return menu_str

    def send_to_admin(self, text=None):
        cache_token = self.mongo.cache.get_key(WX_CACHE_TOKEN)
        if 'value' not in cache_token:
            return 
        token = cache_token['value']
        url = comm.api_const.WXUrl.SERVICE_URL % token
        for admin in self.customers:
            msg = {}
            msg['touser'] = admin
            msg['msgtype'] = 'text' 
            msg['text'] = {'content':text}
            msg_data = json.dumps(msg, ensure_ascii=False).encode('utf-8')
            ret = comm.url_rsp.send_url_request(url, post=msg_data)
            print 'send_rsp:',ret
