#!/usr/bin/python
# -*- coding=utf-8 -*-

import wx_mongo
import wx_xml
from comm.err import IException
from comm.err import ErrCode
from comm.mylogger import MyLogger as LOG
from comm import mytime
import url_mgr

class EventProcessor(object):
    def __init__(self, mongo, logger):
        self.mongo = mongo
        self.log = logger

    def process_event(self, msg, to_id, from_id):
        type = wx_xml.get_wxmsg(msg, 'Event')
        if type == None:
            raise IException(ErrCode.APPErr, 'lack type')

        if type == 'subscribe':
            return self.process_subscribe(msg, to_id, from_id)
        elif type == 'unsubscribe':
            return self.process_unsubscribe(msg, to_id, from_id)
        elif type == 'SCAN':
            return self.process_scan(msg, to_id, from_id)
        elif type == 'LOCATION':
            return self.process_location(msg, to_id, from_id)
        elif type == 'CLICK':
            return self.process_click(msg, to_id, from_id)
        elif type == 'VIEW':
            return self.process_view(msg, to_id, from_id)

    def process_subscribe(self, msg, to_id, from_id):
        self.mongo.user.subscribe(from_id)
        self.mongo.stat.sub(mytime.today2str(), from_id)
        sub_info = 'user %s subscribe me' % from_id
        self.log.info(sub_info)
        umgr = url_mgr.UrlMgr()
        return wx_xml.MsgType.NEWS, url_mgr.UrlMgr().welcomepage()

    def process_unsubscribe(self, msg, to_id, from_id):
        self.mongo.user.unsubscribe(from_id)
        self.mongo.stat.unsub(mytime.today2str(), from_id)
        unsub_info = 'user %s un-subscribe me' % from_id
        self.log.info(unsub_info)
        return wx_xml.MsgType.FORMAT, ''

    def process_scan(self, msg, to_id, from_id):
        key = wx_xml.get_wxmsg(msg, 'EventKey')
        ticket = wx_xml.get_wxmsg(msg, 'Ticket')
        if key == None or ticket == None:
            raise IException(ErrCode.APPErr, 'lack tikcy or key while scan')
        return wx_xml.MsgType.FORMAT, ''

    def process_location(self, msg, to_id, from_id):
        latitude = wx_xml.get_wxmsg(msg, 'Latitude')
        longitude = wx_xml.get_wxmsg(msg, 'Longitude')
        precision = wx_xml.get_wxmsg(msg, 'Precision')
        if latitude == None or longitude == None or precision == None:
            linfo = 'lack latitude longitude or precision while location'
            raise IException(ErrCode.APPErr, linfo)
        return wx_xml.MsgType.FORMAT, ''

    def process_click(self, msg, to_id, from_id):
        key = wx_xml.get_wxmsg(msg, 'EventKey')
        if key == None:
            raise IException(ErrCode.APPErr, 'no button while click')
        umgr = url_mgr.UrlMgr()

        if key in umgr.multi_pages:
            item_arr = umgr.multi_pages[key]
            return wx_xml.MsgType.NEWS, item_arr
        elif key in umgr.pages:
            item_arr = []
            item_arr.append(umgr.pages[key])
            return wx_xml.MsgType.NEWS, item_arr
        else:
            return wx_xml.MsgType.NEWS, umgr.homepage()

    def process_view(self, msg, to_id, from_id):
        url = wx_xml.get_wxmsg(msg, 'EventKey')
        if url == None:
            raise IException(ErrCode.APPErr, 'lack url while view')
        return wx_xml.MsgType.FORMAT, ''


