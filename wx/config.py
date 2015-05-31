#!/usr/bin/python
# -*- coding=utf-8 -*-

from xml.etree import ElementTree
import string
from comm import singleton
from comm.err import ErrCode
from comm.err import IException

ENC_NONE = 0
ENC_COMPATIBLE = 1
ENC_SAFE = 2

@singleton.singleton
class Config(object):
    def __init__(self):
        self.path = ''
        self.token = 'zhengyang_test'

    def load(self, path=None):
        if path is None or not isinstance(path, basestring):
            info = 'config input path is invalid'
            raise IException(ErrCode.ParamErr, info)
        self.path = path

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
        app = tree.find('App')
        self.load_app(app)

        svr = tree.find('WebSvr')
        self.load_websvr(svr)

        db = tree.find('MongoDB')
        self.load_mongo(db)

    def load_app(self, node=None):
        if node is None:
            raise IException(ErrCode.ConfigErr, 'un-find app')
        node_token = node.find('token')
        if node_token is None:
            raise IException(ErrCode.ConfigErr, 'un-find token')
        self.token = node_token.get('val')

        node_appid = node.find('appid')
        if node_appid is None:
            raise IException(ErrCode.ConfigErr, 'un-find token')
        self.appid = node_appid.get('val')

        node_appsecret = node.find('appsecret')
        if node_appsecret is None:
            raise IException(ErrCode.ConfigErr, 'un-find secret')
        self.appsecret = node_appsecret.get('val')

        node_encode = node.find('encode')
        if node_encode is None:
            raise IException(ErrCode.ConfigErr, 'un-find token')
        self.enc_type = string.atoi(node_encode.get('type'))
        self.enc_key = node_encode.get('key')

        node_id = node.find('WXID')
        if node_id is None:
            raise IException(ErrCode.ConfigErr, 'un-find wxid')
        self.id = node_id.get('val')

    def load_websvr(self, node=None):
        if node is None:
            dbinfo = 'WebSvr Element is null in %s' % self.path
            raise IException(ErrCode.ConfigErr, dbinfo)

        self.ip = node.get('ip')
        port = node.get('port')
        if self.ip is None or port is None:
            webinfo = 'ip or port is not find in WebSvr'
            raise IException(ErrCode.ConfigErr, webinfo)
        self.port = string.atoi(port)

    def load_mongo(self, node=None):
        if node is None:
            dbinfo = 'Mongodb Element is null in %s' % self.path
            raise IException(ErrCode.ConfigErr, dbinfo)

        net = node.find('Net')
        if net is None:
            raise IException(ErrCode.ConfigErr, 'un-find mongo_net')
        self.mongo_ip = net.get('ip')
        mongo_port = net.get('port')
        if self.mongo_ip is None or mongo_port is None:
            raise IException(ErrCode.ConfigErr, 'un-find ip or port of mongo')
        self.mongo_port = string.atoi(mongo_port)

        user = node.find('User')
        if user is None:
            userinfo = 'un-find user in mongodb'
            raise IException(ErrCode.ConfigErr, userinfo)
        self.user = user.get('name')

        user_action = node.find('UserAction')
        if user_action is None:
            ainfo = 'un-find user_action in mongodb'
            raise IException(ErrCode.ConfigErr, ainfo)
        self.user_action = user_action.get('name')

        menu = node.find('Menu')
        if menu is None:
            minfo = 'un-find menu in mongodb'
            raise IException(ErrCode.ConfigErr, minfo)
        self.menu = menu.get('name')

        stat = node.find('Stat')
        if stat is None:
            sinfo = 'un-find stat in mongo'
            raise IException(ErrCode.ConfigErr, sinfo)
        self.stat = stat.get('name')

        admin = node.find('Admin')
        if admin is None:
            ainfo = 'un-find admin in mongo'
            raise IException(ErrCode.ConfigErr, ainfo)
        self.admin = admin.get('name')

        cache = node.find('Cache')
        if cache is None:
            cinfo = 'un-find cache in mongo'
            raise IException(ErrCode.ConfigErr, cache)
        self.cache = cache.get('name')

        order = node.find('Order')
        if order is None:
            oinfo = 'un-find order in mongo'
            raise IException(ErrCode.ConfigErr, order)
        self.order = order.get('name')

        shopping = node.find('Shopping')
        if shopping is None:
            oinfo = 'un-find order in mongo'
            raise IException(ErrCode.ConfigErr, order)
        self.shopping = shopping.get('name')

        week_now = node.find('Week_now')
        if week_now is None:
            raise IException(ErrCode.ConfigErr, 'un-find week_now')
        self.week_now = week_now.get('name')

        week_time = node.find('Week_time')
        if week_time is None:
            raise IException(ErrCode.ConfigErr, 'un-find week_time')
        self.week_time = week_time.get('name')


    def to_string(self):
        info = 'config mongo[%s,%d,%s,%s,%s] svr[%s,%d], app[%s,%s,%s,%s,%s]' % (
          self.mongo_ip, self.mongo_port, self.user, 
          self.user_action, self.menu, self.ip, self.port, 
          self.appid, self.appsecret, self.token, self.enc_type, self.enc_key
          )
        return info

if __name__ == '__main__':
    xmlpath = 'wx.xml'
    conf1 = Config()
    try:
        conf1.load(xmlpath)
    except IException as e:
        e.detail()
    else:
        conf1_info = conf1.to_string()
        print conf1_info

    conf2 = Config()
    conf2_info = conf2.to_string() 
    print conf2_info


    xmlpath2 = '../wx.xml'
    conf3 = Config()
    try:
        conf3.load(xmlpath2)
    except IException as e1:
        e1.detail()
        conf3_info = conf3.to_string()
        print conf3_info
    else:
        conf3_info = conf3.to_string()
        print conf3_info

