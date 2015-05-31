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

        wm = tree.find("Wm")
        self.load_wm(wm)

        token_node = tree.find('Token')
        self.load_token(token_node)
        
        customer_node = tree.find('Customer')
        self.load_customer(customer_node)

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
        self.db_name = node.get('db_name')
        port = node.get('port')
        if (self.ip is None or port is None or 
            self.db_name is None):
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

        dc_record = node.find('DCRecode')
        if dc_record is None:
            raise IException(ErrCode.ConfigErr, 'un-find dc_record')
        self.dc_record = dc_record.get('name')

        dc = node.find('DC')
        if dc is None:
            raise IException(ErrCode.ConfigErr, 'un-find dc')
        self.dc = dc.get('name')

    def load_wm(self, node=None):
        if node is None:
            wminfo = 'WM Element is null in %s' % self.path
            raise IException(ErrCode.ConfigErr, wminfo)
        wm_html = node.find('WmHtml')
        if wm_html is None:
            html_info = 'wm html is not found in %s' % self.path
            raise IException(ErrCode.ConfigErr, wm_html)
        self.fpath = wm_html.get('file_path')
        self.pre = wm_html.get('pre')
        self.suf = wm_html.get('suf')
        bnum = int(wm_html.get('begin_num'))
        if (self.fpath is None or self.pre is None or
            self.suf is None or bnum is None):
            load_info = 'lack wm html field in %s' % self.path
            raise IException(ErrCode.ConfigErr, load_info)
        self.bnum = int(bnum)

    def load_token(self, node=None):
        if node is None:
            tinfo = 'token element null in %s' % self.path
	    raise IException(ErrCode.ConfigErr, tinfo)
        self.token_tt = int(node.get('timetick'))
        self.token_tg = int(node.get('timegap'))

    def load_customer(self, node=None):
        if node is None:
            cinfo = 'customer element null %s' % self.path
            raise IException(ErrCode.ConfigErr, cinfo)

        customers = [] 
        candidates = node.findall('person')
        for item in candidates:
            id = item.get('id')
            customers.append(id)
        self.customers = customers

    def to_string(self):
        info = 'config mongo[%s,%d,%s,%s,%s] svr[%s,%d], app[%s,%s,%s,%s,%s]' % (
          self.mongo_ip, self.mongo_port, self.user, 
          self.user_action, self.menu, self.ip, self.port, 
          self.appid, self.appsecret, self.token, self.enc_type, self.enc_key
          )

        wm = ',wm_html_param [%s,%s,%s,%s]' % (self.fpath, 
          self.pre, self.suf, self.bnum)
        tstring = ',token [%d,%d]' % (self.token_tt, self.token_tg)
        return info + wm

if __name__ == '__main__':
    xmlpath = 'wm.xml'
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


    xmlpath2 = '../wm.xml'
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

