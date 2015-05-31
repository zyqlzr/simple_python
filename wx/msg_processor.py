#!/usr/bin/python
# -*- coding=utf-8 -*-

import wx_mongo
import wx_xml

from admin_logic import AdminLogic
from comm.err import IException
from comm.err import ErrCode

class MsgProcessor(object):
    def __init__(self, mongo, logger):
        self.mongo = mongo
        self.log = logger
        self.admin_logic = AdminLogic(mongo, logger)

    def process_text(self, msg, to_id, from_id):
        #print 'MsgProcessor process_text'
        content = wx_xml.get_wxmsg(msg, 'Content')
        if content == None:
            raise IException(ErrCode.APPErr, 'lack context')

        user_pri = self.mongo.admin.find_pri(from_id)
        if user_pri is None:
            return self.admin_logic.process_fanyoyo(from_id, content)
        else:
            return self.admin_logic.process_text(from_id, user_pri, content)
 
    def process_image(self, msg, to_id, from_id):
        pic_url = wx_xml.get_wxmsg(msg, 'PicUrl')
        media_id = wx_xml.get_wxmsg(msg, 'MediaId')
        if pic_url == None or media_id == None:
            raise IException(ErrCode.APPErr, 'lack url or id') 
        return None

    def process_voice(self, msg, to_id, from_id):
        media_id = wx_xml.get_wxmsg(msg, 'MediaId')
        format = wx_xml.get_wxmsg(msg, 'Format')
        if media_id == None:
            raise IException(ErrCode.APPErr, 'lack id') 
        return None

    def process_video(self, msg, to_id, from_id):
        return None

    def process_location(self, msg, to_id, from_id):
        return None

    def process_link(self, msg, to_id, from_id):
        return None 


