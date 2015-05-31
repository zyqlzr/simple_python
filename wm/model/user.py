#!/usr/bin/python
# -*- coding=utf-8 -*-

import pymongo
from comm.err import ErrCode
from comm.err import IException

SCHEMA_USER = """
schema:
{
  "__id": "wx_id"
  "stat": True
  "lastest_info": 
    {
      "phone": "13912561987" 
      "area": 0
      "addr": 
    }
}
"""

class User(object):
    def __init__(self, coll=None):
        if coll is None or not isinstance(coll, pymongo.collection.Collection):
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll = coll
        if self.coll.count() == 0:
            self.init_coll()

    def init_coll(self, user="", stat=False):
        self.coll.insert({"_id":user, "lastest_info":{}, 'stat':stat})

    def subscribe(self, user=None):
        if user is None:
            raise IException(ErrCode.ParamErr, 'input user is null')
        u = self.coll.find_one({'_id':user}) 
        if u is None:
            self.init_coll(user, True)
        else:
            self.coll.update({"_id":user}, {"$set": {'stat':True}}) 

    def unsubscribe(self, user=None):
        if user is None:
            raise IException(ErrCode.ParamErr, 'input user is null')
        u = self.coll.find_one({"_id":user})
        if u is None:
            self.init_coll(user)
        else:
            self.coll.update({"_id":user}, {"$set": {"stat":False}})

    def update(self, user=None, area=None, phone=None, addr=None):
        if user is None or area is None or phone is None or addr is None:
            raise IException(ErrCode.ParamErr, 'param of update is null')
        val = {"phone":phone, "area":area, "addr":addr}
        self.coll.update({"_id":user}, {"$set":{"lastest_info":val}}, upsert=True)

    def find(self, user=None):
        return self.coll.find_one({'_id':user})

    def find_user_info(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'param of update is null')
        cursor = self.coll.find({'_id':id}, {'_id':0, 'lastest_info':1})
        if 1 != cursor.count():
            return False, None
        return True, cursor[0] 

    def find_last_info(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'input null')
        return self.coll.find_one({'_id':id}, {'_id':0,'lastest_info':1})

    def drop(self):
        self.coll.drop()

    def schema(self):
        return SCHEMA_USER

