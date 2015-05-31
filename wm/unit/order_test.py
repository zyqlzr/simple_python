#!/usr/bin/python
# -*- coding=utf-8 -*-

import time
import json
import pymongo
import config
import wx_mongo
import order_notify

from model import stat
from model import mongodb
from model import user
from model import admin

from comm.mylogger import MyLogger as LOG
from comm import mytime
from comm.err import IException
from comm import err

from wx_mongo import WxMongo
from order_mgn import OrderMgn

def order_test():
    conf = config.Config()
    conf.load('./unit/test.xml')
    print conf.to_string()
    print("%s,%d", conf.mongo_ip, conf.mongo_port)
    conn = pymongo.Connection(host=conf.mongo_ip, port=conf.mongo_port, network_timeout=10)
    print 'connection ok'
    try:
        db = mongodb.WxDatabase(conn)
        db_user = user.User(db.get_collection(conf.user))
    except IException as e:
        e.detail()
        return None
    print 'user coll ok'

    db_user.update('zhengyang', 0, '18757571517', 'xl area')
    db_user.update('zhengyang', 0, '18757571517', 'xf street')
    db_user.update('jianglili', 0, '15268526565', 'xl area')
    db_user.update('jianglili', 0, '15268526565', 'xf street')

    cursor = db_user.coll.find({})
    for ele in cursor:
        print ele

    wx_mongo.WxMongo().start()
    omgn = OrderMgn()
    omgn.init()
    access_text = {'openid':'zhengyang'}
    access_input = json.dumps(access_text)
    print omgn.get_order_html(access_input)

def user_find_test():
    conf = config.Config()
    conf.load('./unit/test.xml')
    print conf.to_string()
    print("%s,%d", conf.mongo_ip, conf.mongo_port)
    conn = pymongo.Connection(host=conf.mongo_ip, port=conf.mongo_port, network_timeout=10)
    print 'connection ok'
    try:
        db = mongodb.WxDatabase(conn)
        db_user = user.User(db.get_collection(conf.user))
    except IException as e:
        e.detail()
        return None
    print 'user coll ok'

    wx_mongo.WxMongo().start()
    omgn = OrderMgn()
    omgn.init()
    info = omgn.get_user_info('zzzz')
    print type(info)
    print info


def order_token():
    conf = config.Config()
    conf.load('./unit/test.xml')

    log = LOG()
    mongo = wx_mongo.WxMongo()
    log.setlogger('./test.log')
    mongo.start()

    refresher = order_notify.TokenRefresher()
    refresher.start_refresh(LOG().getlogger(), mongo, conf)
    time.sleep(60)
    refresher.stop_refresh()


def order_and_shopping():
    conf = config.Config()
    conf.load('./unit/test.xml')

    log = LOG()
    mongo = wx_mongo.WxMongo()
    log.setlogger('./test.log')
    mongo.start()

    oid = 'zhengyang'
    odtime = mytime.today2str()
    oprice = '14'
    ocounts = [1, 2, 3, 4, 5, 6, 7, 8]
    for i in ocounts:
        omenu = {}
        omenu['m'] = 'menu' + str(i)
        omenu['n'] = i
        omenu['t'] = 'title' + str(i)
        mongo.order.add_order(id=oid, dtime=odtime, 
            count=i, menu=omenu, price=oprice)
        mongo.shopping.add_shopping(id=oid, dtime=odtime, count=i)

    nums = mongo.shopping.get_shopping(oid)
    print nums
    id_arrays = nums['history']
    for id in id_arrays:
        id_order = mongo.order.get_order(id)
        print id_order


    arr_len = len(id_arrays)
    print id_arrays[arr_len - 4]
    print id_arrays[arr_len - 3]
    print id_arrays[arr_len - 2]

    mongo.shopping.drop()
    mongo.order.drop()

def order_history_test():
    conf = config.Config()
    conf.load('./unit/test.xml')

    mongo = wx_mongo.WxMongo()
    mongo.start()
    oid = 'zhengyang'
    odtime = mytime.today2str()
    oprice = '14'
    ocounts = [1, 2, 3, 4, 5, 6, 7, 8]
    for i in ocounts:
        omenu_arr = []
        omenu = {}
        omenu['m'] = 'menu' + str(i)
        omenu['n'] = i
        omenu['t'] = 'title' + str(i)
        omenu_arr.append(omenu)
        mongo.order.add_order(id=oid, dtime=odtime, 
            count=i, menu=omenu_arr, price=oprice)
        mongo.shopping.add_shopping(id=oid, dtime=odtime, count=i)

    omgn = OrderMgn()
    omgn.init()
    access_text = {'openid':'zhengyang'}
    access_input = json.dumps(access_text)
    print omgn.get_order_history_html(access_input)
    mongo.shopping.drop()
    mongo.order.drop()

