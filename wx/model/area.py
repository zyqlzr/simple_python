#!/usr/bin/python
# -*- coding=utf-8 -*-

import pymongo
from comm.err import ErrCode
from comm.err import IException

SCHEMA_AREA = """
schema:
{
  "_id": area_id
  "addr": "yk-garden"
  "position":
    {
      "location_x": 23.134521
      "location_y": 113.358803
    }
  "range":xxxx
}
"""

class Area(object):
    def __init__(self, coll=None):
        if coll is None or not isinstance(coll, pymongo.collection.Collection):
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll = coll
        if self.coll.count() == 0:
            self.init_coll()

    def init_coll(self, area=0)
        pos = {'location_x': 0.0, 'location_y': 0.0}
        area_info = {'id':0, 'addr':'heart', 'position': pos, 'range': 0.0}
        self.coll.insert(area_info)

    def add_area(self, area=None, addr=None, pos_x=0.0,
                 pos_y=0.0, range=0.0):
        if (area is None or addr is None):
            raise IException(ErrCode.ParamErr, 'coll is null')
        self.coll.insert({'_id': area, 'addr':addr,
                          'position':{'location_x': pos_x, 'location_y': pos_y}, 
                          'range': range})

    def del_area(self, area=None):
        if area is None:
            raise IException(ErrCode.ParamErr, 'area is null while del')
        self.coll.remove({'_id':area})

    def update_area(self, area=None, addr=None, 
                    pos_x=None, pos_y=None, range=None):
        if area is None:
            raise IException(ErrCode.ParamErr, 'area is none while update')
 
        area_info = {'area': area}
        if addr != None:
            area_info['addr'] = addr
        if pos_x != None and pos_y != None:
            area_info['position'] = {'location_x': pos_x, 'location_y': pos_y}
        if range != None:
            area_info['range'] = range 
        self.coll.update(area_info)

    def schema():
        return SCHEMA_AREA
