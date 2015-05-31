#!/usr/bin/python
# -*- coding=utf-8 -*-

import pymongo
import config
from event_processor import EventProcessor

from model import stat
from model import mongodb
from model import user
from model import admin

from comm.mylogger import MyLogger as LOG
from comm import mytime
from comm.err import IException
from comm import err

from admin_logic import AdminLogic
from wx_mongo import WxMongo

import time
import url_mgr

def db_test():
    try:
        db = mongodb.WxDatabase()
    except err.IException as db_err:
        db_err.detail()
    else:
        print "no exception"

class SingleTest(object):
    counter = 0
    def add_count(self, num):
        self.counter += num;

def singleton_test():
    test1 = SingleTest()
    test2 = SingleTest()
    test3 = SingleTest()
    test1.add_count(1)
    test2.add_count(5)
    print test3.counter

def time_test():
    now = time.localtime()
    print now
    now1 = time.gmtime()
    print now1
    info = '%s_%s_%s' % (now1[0], now1[1], now1[2])
    print info
    print mytime.today2str()

def stat_test():
    conf = config.Config()
    conf.load('./unit/test.xml')
    print conf.to_string()
    print("%s,%d", conf.mongo_ip, conf.mongo_port)
    conn = pymongo.Connection(host=conf.mongo_ip, port=conf.mongo_port, network_timeout=10)
    print 'connection ok'
    try:
        db = mongodb.WxDatabase(conn)
        stat = stat.Stat(db.get_collection(conf.sub))
    except IException as e:
        e.detail()
        return None
    print 'stat coll ok'

    stat.sub(mytime.today2str(), '105789990')
    stat.sub(mytime.today2str(), '105789991')
    print stat.find(mytime.today2str())
    stat.drop()

    stat.unsub(mytime.today2str(), '105789990')
    stat.unsub(mytime.today2str(), '105789991')
    print stat.find(mytime.today2str())
    stat.drop()

def user_test():
    conf = config.Config()
    conf.load('./unit/test.xml')
    print("%s,%d", conf.mongo_ip, conf.mongo_port)
    conn = pymongo.Connection(host=conf.mongo_ip, port=conf.mongo_port, network_timeout=10)
    print 'connection ok'
    try:
        db = mongodb.WxDatabase(conn)
        user_coll = user.User(db.get_collection(conf.user))
    except IException as e:
        e.detail()
        return None

    print '*****subscribe test*****'
    user_coll.subscribe('105789992')
    user_coll.subscribe('105789993')
    for item in user_coll.coll.find():
        print item

    print '*****unsubscribe test*****'
    user_coll.unsubscribe('105789992')
    user_coll.unsubscribe('105789993')
    for uitem in user_coll.coll.find():
        print uitem

    print '*****update test*****'
    user_coll.update('105789994', 0, '18757571518', 'streat'
)
    user_coll.update('105789994', 1, '18757571518', 'city')
    for aitem in user_coll.coll.find():
        print aitem

    print 'user[%s] find in coll is %s' % ('105789994', user_coll.find('105789994'))
    user_coll.drop();

FOOD_1 = u'土豆牛肉'

FOOD_2 = u'水煮肉片' 

FOOD_3 = u'火爆大头菜' 


def admin_logic_test():
    conf = config.Config()
    conf.load('./unit/test.xml')

    umgr = url_mgr.UrlMgr()
    umgr.init('./url.xml', None)
    umgr.load()

    print 'mongo ip=%s,port=%d' % (conf.mongo_ip, conf.mongo_port)
    mongo = WxMongo()
    mongo.start()
    LOG().setlogger('./log')
    log = LOG().getlogger()

    admin_logic = AdminLogic(mongo, log)
    eventp = EventProcessor(mongo, log)

    admin_coll = mongo.admin
    user_coll = mongo.user
    stat_coll = mongo.stat
    menu_coll = mongo.menu

    for aitem in admin_coll.coll.find():
        print aitem
    #admin_coll.coll.drop()
    fid = 'test_zhengyang'
    tid = 'zyqlzr'
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'sub')

    msg = ''
    print eventp.process_subscribe(msg, 'ifanyoyo', 'test_1')
    print eventp.process_subscribe(msg, 'ifanyoyo', 'test_2')
    print eventp.process_subscribe(msg, 'ifanyoyo', 'test_2')
    print eventp.process_subscribe(msg, 'ifanyoyo', 'test_3')
    print eventp.process_subscribe(msg, 'ifanyoyo', 'test_4')
    print eventp.process_unsubscribe(msg, 'ifanyoyo', 'test_3')
    print eventp.process_unsubscribe(msg, 'ifanyoyo', 'test_4')
    print eventp.process_unsubscribe(msg, 'ifanyoyo', 'test_5')

    today = mytime.today2str()
    menu_coll.add_menu(name='menu_1', day=today, price=10, title=FOOD_1, 
            url='http://127.0.0.1/menu1', info='balabala1', clock=0)
    menu_coll.add_menu(name='menu_2', day=today, price=10, title=FOOD_2, 
            url='http://127.0.0.1/menu2', info='balabala2', clock=0)
    menu_coll.add_menu(name='menu_3', day=today, price=10, title=FOOD_3, 
            url='http://127.0.0.1/menu3', info='balabala3', clock=0)


    admin_coll.add_admin(user='jll270626101', pri=10, name='jianglili')
    #admin_coll.add_admin(user='x351575427', pri=8, name='jiangzifa')
    #admin_coll.add_admin(user='employee_1', pri=5, name='zhangsan')
    #admin_coll.add_admin(user='employee_2', pri=5, name='lisi')
    #admin_coll.add_admin(user='client_1', pri=0, name='wangwu')
    #admin_coll.add_admin(user='client_2', pri=0, name='zhaoliu')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'add admin x351575427 jiangzifa')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'add employee employee_1 zhangsan')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'add employee employee_2 lisi')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'add employee employee_3 zhengqi')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'add employee employee_4 zhengqi')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'add client client_1 wangwu')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'add client client_2 zhaoliu')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'add client client_3 zhaoliu')

    for uitem in user_coll.coll.find():
        print uitem
    for sitem in stat_coll.coll.find():
        print sitem
    for aitem in admin_coll.coll.find():
        print aitem

    print admin_logic.process_text(fid, admin.PRI_ROOT, 'sub')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'sub +')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'sub -')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'unsub')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'unsub +')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'unsub -')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'unsub')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'menu')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'menu +')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'menu -')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'list all')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'list admin')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'list employee')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'list client')

    print admin_logic.process_text(fid, admin.PRI_ROOT, 'del wx employee_2')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'del name zhaoliu')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'del employee_4 zhengqi')

    print admin_logic.process_text(fid, admin.PRI_ROOT, 'list employee')
    print admin_logic.process_text(fid, admin.PRI_ROOT, 'list client')

    admin_coll.coll.drop()
    user_coll.coll.drop()
    stat_coll.coll.drop()
    menu_coll.coll.drop()


