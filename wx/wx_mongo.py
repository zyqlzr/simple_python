#!/usr/bin/python
# -*- coding=utf-8 -*-

import pymongo
import config
from comm import singleton
from model import admin
from model import stat
from model import menu
from model import user
from model import cache
from model import order
from model import mongodb 

@singleton.singleton
class WxMongo(object):
    def __init__(self):
        pass

    def start(self):
        conf = config.Config()
        self.conn = pymongo.Connection(host=conf.mongo_ip,
            port=conf.mongo_port, network_timeout=10)
        self.db = mongodb.WxDatabase(self.conn)

        self.user = user.User(self.db.get_collection(conf.user)) 
        self.stat = stat.Stat(self.db.get_collection(conf.stat))
        self.menu = menu.Menu(self.db.get_collection(conf.menu))
        self.week_now = menu.WeekNow(self.db.get_collection(conf.week_now))
        self.week_time = menu.WeekTime(self.db.get_collection(conf.week_time))
        self.admin = admin.Admin(self.db.get_collection(conf.admin))
        self.cache = cache.Cache(self.db.get_collection(conf.cache))
        self.order = order.Order(self.db.get_collection(conf.order))
        self.shopping = order.Shopping(self.db.get_collection(conf.shopping))
