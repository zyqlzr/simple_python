#!/usr/bin/python
# -*- coding=utf-8 -*-

import pymongo
import time
from comm.err import ErrCode
from comm.err import IException
from pymongo.errors import PyMongoError as MongoErr

class WxDatabase(object):
    DEF_DBNAME = 'ymw'
    def __init__(self, conn=None, dbname=None):
        if conn is None:
            raise IException(ErrCode.TypeErr, "conn is null")
        if not isinstance(conn, pymongo.Connection):
            raise IException(ErrCode.TypeErr, "conn type err")
        self.conn = conn
        self.conn.write_concern = {'w': 1, 'wtimeout':1000, 'j': True}

        if dbname == None or not isinstance(dbname, basestring):
            self.db_name = self.DEF_DBNAME
        else:
            self.db_name = dbname 

        self.db = self.conn[self.db_name]

    def get_collection(self, name=None):
        if name is None or not isinstance(name, basestring):
            raise IException(ErrCode.ParamErr, "input collection name err")

        coll = None
        coll = self.db[name]
        return coll


