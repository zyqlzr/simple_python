#!/usr/bin/python
# -*- coding=utf-8 -*-

import pymongo
from comm.err import ErrCode
from comm.err import IException

SCHEMA_CACHE = """
schema:
{
  "_id": key
  "value": xxxxx
}
"""

class Cache(object):
    def __init__(self, coll=None):
        if coll is None or not isinstance(coll, pymongo.collection.Collection):
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll = coll

    def set_key(self, key=None, value=None):
        if key is None:
            raise IException(ErrCode.ParamErr, 'key is input null')
        if value is None:
            raise IException(ErrCode.ParamErr, 'value is input null')
        self.coll.update({'_id':key}, {'$set':{'value': value}}, upsert=True)

    def get_key(self, key=None):
        if key is None:
            raise IException(ErrCode.ParamErr, 'input null')
        return self.coll.find_one({'_id':key})




