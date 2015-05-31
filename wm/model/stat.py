#!/usr/bin/python
# -*- coding=utf-8 -*-

import pymongo
from comm import mytime
from comm.err import ErrCode
from comm.err import IException

SCHEMA_STAT = """
schema:
{
  "_id":"2015_01_15"
  "subscribe": 
    [ 
      "wx_id1"
      "wx_id2"
    ]

  "unsubscribe":
    [
      "wx_id3"
      "wx_id4"
    ]

   "order":
   [
     ObjectId1
     ObjectId2
   ]
}
"""

class Stat(object):
    def __init__(self, coll=None):
        if coll is None or not isinstance(coll, pymongo.collection.Collection):
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll = coll
        if self.coll.count() == 0:
            self.init_coll()

    def init_coll(self):
        id = ''
        self.coll.insert({'_id':id, "subscribe":[], "unsubscribe":[]})

    def sub(self, day=None, user=None):
        if day is None or user is None:
            raise IException(ErrCode.ParamErr, 'input is null')
        #print day,user
        self.coll.update({'_id':day}, {"$addToSet": {"subscribe":user}}, upsert=True)

    def unsub(self, day=None, user=None):
        if day is None or user is None:
            raise IException(ErrCode.ParamErr, 'input is null')
        #print day,user
        self.coll.update({'_id':day}, {"$addToSet": {"unsubscribe":user}}, upsert=True)


    def find(self, key=None):
        if key is None:
            raise IException(ErrCode.ParamErr, 'input is null')
        return self.coll.find_one({"_id":key})

    def find_all(self):
        pass

    def find_sub(self, key=None):
        if key is None:
            raise IException(ErrCode.ParamErr, 'input is null')
        subs = self.coll.find_one({'_id':key}, {'_id': 0, 'subscribe': 1})
        if subs is None or 'subscribe' not in subs:
            return []
        else:
            return subs['subscribe']

    def find_unsub(self, key=None):
        if key is None:
            raise IException(ErrCode.ParamErr, 'input is null')
        unsubs = self.coll.find_one({'_id':key}, {'_id': 0, 'unsubscribe': 1})
        if unsubs is None or 'unsubscribe' not in unsubs:
            return None
        else:
            return unsubs['unsubscribe']

    def order(self, day=None, order_id=None):
        if day is None or order_id is None:
            raise IException(ErrCode.ParamErr, 'input is null')
        self.coll.update({'_id':day}, {"$push": {"order": order_id}}, upsert=True) 

    def find_order(self, key=None):
        if key is None:
            raise IException(ErrCode.ParamErr, 'input is null')
        orders = self.coll.find_one({'_id':key}, {'_id': 0, 'order': 1})
        if orders is None or 'order' not in orders:
            return []
        else:
            return orders['order']
 
    def drop(self):
        self.coll.drop()

    def schema(self):
        return SCHEMA_STAT 


