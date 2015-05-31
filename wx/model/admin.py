#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
import pymongo
from pymongo.errors import PyMongoError as MongoErr
from comm import mytime
from comm.err import ErrCode
from comm.err import IException

SCHEMA_ADMIN = """
schema:
{
  "_id"="wx_id"
  "pri"= int
  "name" = ""
}
privilege value:
ROOT = 10 
ADMIN = 8 
EMPLOYEE = 5
CLIENT = 0
"""

DEF_ROOT = 'o1iT9jkFTT98b9y8mBz04nS93m98'
PRI_ROOT = 10 
PRI_ADMIN = 8 
PRI_EMPLOYEE = 5
PRI_CLIENT = 0

class Admin(object): 
    def __init__(self, coll=None):
        if coll is None or not isinstance(coll, pymongo.collection.Collection):
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll = coll
        if self.coll.count() == 0:
            self.init_coll()

    def init_coll(self):
        self.coll.insert({'_id': DEF_ROOT, 'pri':PRI_ROOT, 'name':'zhengyang'})

    def add_admin(self, user=None, pri=None, name=''):
        if user is None or pri is None:
            raise IException(ErrCode.ParamErr, 'user or pri is null')
        return self.coll.insert({'_id':user, 'pri':pri, 'name':name})

    def del_admin(self, user=None, name=None):
        if user is None and name is None:
            raise IException(ErrCode.ParamErr, 'input user is null')
        input = {}
        if user is not None:
            input['_id'] = user
        if name is not None:
            input['name'] = name
        if 0 == len(input):
            return
        return self.coll.remove(input)

    def update_admin(self, name=None, pri=None):
        if name is None and pri is None:
            raise IException(ErrCode.ParamErr, 'name or pri is null')
        return self.coll.update({'name': name}, {"$set":{'pri':pri}})

    def find_name(self, name=None):
        if name is None:
            raise IException(ErrCode.ParamErr, 'name is null')
        cursor = self.coll.find({'name': name}, {'_id':1, 'pri':1})
        zys = []
        if 0 == cursor.count():
            return None 
        for ele in cursor:
            zys.append(ele)
        return zys

    def find_pri(self, user=None):
        if user is None:
            raise IException(ErrCode.ParamErr, 'user is null')

        user_doc = self.coll.find_one({'_id':user}, {'_id':0, 'pri':1})
        if user_doc is None:
            return None
        else:
            return user_doc['pri']

    def find_admin(self, pri=None):
        q_pri = {}
        if pri is not None:
            q_pri = {'pri':pri}
        a_cursor = self.coll.find(q_pri, {'_id':1, 'name':1})
        if 0 == a_cursor.count():
            return None
        admin_list = []
        try:
            for ele in a_cursor:
                #print ele 
                if not isinstance(ele, dict):
                    continue
                tmp = json.dumps(ele, indent=1, ensure_ascii=False).encode('utf-8')
                admin_list.append(tmp)
            return admin_list
        except KeyError:
            return None

    def schema(self):
        return SCHEMA_ADMIN


