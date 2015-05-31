#!/usr/bin/python
# -*- coding=utf-8 -*-

import pymongo
from comm.err import ErrCode
from comm.err import IException
import datetime

SCHEMA_ORDER = """
order_schema:
{
  "_id": "2015-01-15:8"
  'oid': openid
  'p': 0,               //price
  'menu': [
     {
       'm': menu_id,         //menu number
       'n': 2,               //order counter
       't': "bouillabaisse", //title
     },
     .....
   ],
   't': 0                  //type of order, 0 now, 1 time
   ......
}

week_schema:
{
  "_id": openid
   'history': [
      date:num,
      ...... 
    ],
}
"""

class OrderType(object):
    OrderNow = 0
    OrderTime = 1

class Order(object):
    def __init__(self, coll=None):
        if coll is None or not isinstance(coll, pymongo.collection.Collection):
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll = coll

    def add_order(self, id=None, order_id=None, menu=[], price=0, type=0):
        if (id is None or order_id is None):
            raise IException(ErrCode.ParamErr, 'param is null')
        self.coll.update({'_id': order_id}, 
            {"$set": {'oid':id, 'p':price, 'menu':menu, 't':type}}, upsert=True)

    def get_order(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'param is null')
        return self.coll.find_one({'_id': id})

    def drop(self):
        self.coll.drop()

class Shopping(object):
    def __init__(self, coll=None):
        if coll is None or not isinstance(coll, pymongo.collection.Collection):
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll = coll

    def add_shopping(self, id=None, order_id=None):
        if (id is None or order_id is None):
            raise IException(ErrCode.ParamErr, 'param is null')
        self.coll.update({'_id': id}, {"$push": {'history': order_id}}, upsert=True)

    def get_shopping(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'param is null')
        return self.coll.find_one({'_id': id}, {'_id':0, 'history':1})

    def drop(self):
        self.coll.drop()

