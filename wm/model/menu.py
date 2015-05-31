#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
import pymongo
from comm.err import ErrCode
from comm.err import IException

SCHEMA_MENU = """
schema:
{
  '_id': xxx,
  'price': 12,
  'title': xxxxxx,
  'type': 0,
  'purl': http:://www.xxxx.cn/xxxx,
  'max': 10,
  'des': xxxxxxx,
  'count': 0
}
"""

SCHEMA_WEEK_NOW_MENU = """
schema:
{
  "_id": now_weekday,   //now_1
  "menu": [
    {
      'id': xxx,
      'price': 12,
      'title': xxxxxx,
      'discount': 0,
      'type': 0,
      'purl': http:://www.xxxx.cn/xxxx,
      'max': 10,
      'des': xxxxxxxx
    },
    ....
  ],

  "menu_id_arr": [
    menu_id1,
    menu_id2,
    .....
    menu_idN
  ]
}
"""

SCHEMA_WEEK_TIME_MENU = """
schema:
{
  "_id": time_day("time_1"),
  "menu": [
    {
      'id': xxx,
      'price': 12,
      'title': xxxxxx,
      'discount': 1,
      'type': 0,
      'purl': http:://www.xxxx.cn/xxxx,
      'max': 10,
      'des': xxxxxx
    },
    ....
  ],

  "menu_id_arr": [
    menu_id1,
    menu_id2,
    .....
    menu_idN
  ]
}
"""

MENU_NOW_PRE='now_'
MENU_TIME_PRE='time_'

class MenuType(object):
    WMRecommend = 0
    WMChaocai = 1
    WMDrink = 2

class Menu(object):
    def __init__(self, coll=None):
        if coll is None or not isinstance(coll, pymongo.collection.Collection):
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll = coll

    def add_menu(self, id=None, price=None, title=None, 
            type=MenuType.WMRecommend, purl='', max=0, des=''):
        if id is None or price is None or title is None:
            raise IException(ErrCode.ParamErr, 'input is null')
        self.coll.insert({'_id':id, 'price':price, 'title':title, 
            'type':type, 'purl':purl, 'max':max, 'des':des, 'count':0})

    def update_menu(self, id=None, price=None, title=None, 
            type=MenuType.WMRecommend, purl="", max=0, des=''):
        if (id is None or price is None or title is None):
            raise IException(ErrCode.ParamErr, 'input is null')
        self.coll.update({'_id':id}, 
            {"$set": {'price':price, 'title':title, 'type':type, 'purl':purl, 'max':max, 'des':des}}, 
            upsert=True)

    def inc_menu(self, id=None, num=1):
        if id is None:
            raise IException(ErrCode.ParamErr, 'input is invalid')
        self.coll.update({'_id':id}, {"$inc": {'count': num}}, upsert=True)

    def get_menu(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, "day is null")
        return self.coll.find_one({'_id': id})

    def schema(self):
        return SCHEMA_MENU

class WeekNow(object):
    def __init__(self, coll=None):
        if coll is None or not isinstance(coll, pymongo.collection.Collection):
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll = coll

    def add_menu(self, id=None, menu={}):
        if ('id' not in menu or 'price' not in menu or
            'title' not in menu or 'discount' not in menu or
            'max' not in menu or 'type' not in menu or 
            'purl' not in menu):
            raise IException(ErrCode.ParamErr, 'menu lack kv')
        self.coll.update({'_id':id}, {"$push":{'menu':menu, 'menu_id_arr':menu['id']}}, upsert=True)

    def update_weekmenu(self, id=None, menus=[], menu_ids=[]):
        if id is None:
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll.update({'_id':id}, {"$set":{'menu':menus, 'menu_id_arr':menu_ids}}, upsert=True)

    def get_weekmenu(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'coll is null')
        return self.coll.find_one({'_id':id}, {'_id': 0, 'menu':1})

    def get_weekids(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'id is null')
        return self.coll.find_one({'_id':id}, {'_id':0, 'menu_id_arr': 1})

    def get_weekall(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'coll is null')
        return self.coll.find_one({'_id':id})


class WeekTime(object):
    def __init__(self, coll=None):
        if coll is None or not isinstance(coll, pymongo.collection.Collection):
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll = coll

    def add_menu(self, id=None, menu={}):
        if ('id' not in menu or 'price' not in menu or
            'title' not in menu or 'discount' not in menu or
            'max' not in menu or 'type' not in menu or 
            'purl' not in menu):
            raise IException(ErrCode.ParamErr, 'menu lack kv')
        self.coll.update({'_id': id}, {"$push":{'menu':menu, 'menu_id_arr':menu['id']}})

    def update_weektime(self, id=None, menus=[], menu_ids=[]):
        if id is None:
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll.update({'_id': id}, {"$set":{'menu':menus, 'menu_id_arr':menu_ids}}, upsert=True)

    def get_weektime(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'coll is null')
        return self.coll.find_one({'_id': id}, {'_id': 0, 'menu':1})

    def get_weekids(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'id is null')
        return self.coll.find_one({'_id': id}, {'_id': 0, 'menu_id_arr': 1})

    def get_weekall(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'coll is null')
        return self.coll.find_one({'_id': id})

