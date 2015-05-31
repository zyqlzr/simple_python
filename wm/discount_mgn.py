#!/usr/bin/python
# -*- coding=utf-8 -*-

from xml.etree import ElementTree
import string
from comm import singleton
from comm.err import ErrCode
from comm.err import IException
import wx_mongo

@singleton.singleton
class DiscountMgn(object):
    discounts = {'0': {'type': 0, 'price': 0, 'title':''}}
    path = ''

    def start(self, path):
        self.mongo = wx_mongo.WxMongo()
        self.load(path)
        self.update_db()

    def discount(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'input openid is invalid')
        dc_r = self.mongo.dc_record.get_record(id)
        print dc_r
        if dc_r is None or dc_r['first'] is False:
            return self.discounts['1'] 
        else:
            return self.discounts['2']

    def discount_first_check(self, id=None):
        if id is None:
            raise IException(ErrCode.ParamErr, 'input openid is invalid')
        self.mongo.dc_record.set_first(id) 

    def load(self, path):
        if path is None or not isinstance(path, basestring):
            info = 'dc.xml path is invalid'
            raise IException(ErrCode.ParamErr, info)
        self.path = path
        print self.path

        tree = None
        try:
            with open(self.path, 'rt') as f:
                tree = ElementTree.parse(f)
        except IOError:
            io_info = 'open %s failed' % path
            raise IException(ErrCode.ThirdErr, io_info)

        if tree is None:
            cinfo = 'parse xml %s failed' % self.path
            raise IException(ErrCode.ConfigErr, cinfo)

        dc_node = tree.find('DC')
        self.load_dc(dc_node)

    def load_dc(self, dc_node = None):
        if dc_node is None:
            raise IException(ErrCode.ParamErr, 'input invalid')
        dcs = dc_node.findall('discount')
        for dc in dcs:
            type = dc.get('type')
            price = int(dc.get('price'))
            title = dc.get('title')
            self.discounts[type] = {'type':int(type), 'price':price, 'title':title}
        print self.discounts

    def update_db(self):
        for dc in self.discounts:
            dc_ele = self.discounts[dc]
            if ('type' not in dc_ele or 'price' not in dc_ele or 'title' not in dc_ele):
                continue
            print 'add discount,',dc_ele
            self.mongo.dc.add_discount(dc_ele['type'], dc_ele['price'], dc_ele['title'])


if __name__ == "__main__":
    dm = DiscountMgn()
    dm.load('./dc.xml')


