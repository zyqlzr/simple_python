#!/usr/bin/python
# -*- coding=utf-8 -*-

import pymongo
from comm.err import ErrCode
from comm.err import IException

SCHEMA_DISCOUNT = """
schema:
{
  "_id": openid,
  "first": True,
}

discount_schema:
{
  "_id": id   , //type field in xml
  "price": 0  , //
  "title": xxx, //describe of discount
}
"""

class DiscountRecord(object):
    def __init__(self, coll=None):
        if coll is None or not isinstance(coll, pymongo.collection.Collection):
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll = coll

    def get_record(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'oid is null')
        return self.coll.find_one({'_id': id})

    def set_first(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'oid is null')
        self.coll.update({'_id':id}, {"$set": {'first':True}}, upsert=True)

class Discount(object):
    def __init__(self, coll=None):
        if coll is None or not isinstance(coll, pymongo.collection.Collection):
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll = coll

    def add_discount(self, id=None, price=0, title=''):
        if id is None:
            raise IException(ErrCode.ParamErr, 'oid is null')
        self.coll.update({'_id': id}, {"$set": {'price': price, 'title':title}}, upsert=True)

    def get_discount(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'oid is null')
        return self.coll.find_one({'_id': id})


