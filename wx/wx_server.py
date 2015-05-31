#!/usr/bin/python
# -*- coding=utf-8 -*-

import config
import wx_xml
import msg_processor
import event_processor

import datetime
import json
import os
import sys
import hashlib
import time
import wx_mongo

from comm.err import IException
from comm.err import ErrCode
from comm import singleton 
from comm.mylogger import MyLogger as LOG
from crypto.WXBizMsgCrypt import WXBizMsgCrypt

@singleton.singleton
class WxServer(object):
    ENCODE_AES = 'aes'
    DEF_NONCE = '1234567890'
    def __init__(self):
        self.conf = config.Config()

    def start(self, path=None):
        if path is None:
            pinfo = 'input path is null of WxServer'
            raise err.IException(err.ErrCode.ParamErr, pinfo)
        self.conf.load(path)
        wx_mongo.WxMongo().start()
        self.log = LOG().getlogger()
        self.mprocessor = msg_processor.MsgProcessor(wx_mongo.WxMongo(), self.log)
        self.eprocessor = event_processor.EventProcessor(wx_mongo.WxMongo(), self.log)
        self.wx_crypto = WXBizMsgCrypt(self.conf.token, self.conf.enc_key, self.conf.appid)

    """
    Dispatch msg to processor.
    """
    def do_request(self, args, body):
        arg_num = len(args)
        if 0 == arg_num:
            return self.process_body(body)
        elif config.ENC_NONE == self.conf.enc_type:
            return self.process_normal(args, body)
        else:
            return self.process_encode(args, body)

    def process_normal(self, args, doc):
        #print 'process_normal'
        try:
            nonce = args['nonce'][0]
            timestamp = args['timestamp'][0]
            signature = args['signature'][0]
        except KeyError:
            self.log.error('lack argus')
            return ''
        if not self.check_signature(signature, timestamp, nonce, self.conf.token):
            self.log.error('check signature failed')
            return ''

        return self.process_body(doc)

    def process_body(self, doc):
        #print 'process_body'
        try:
            msg = wx_xml.wxxml2dict(doc)
        except IException as e:
            e.detail()
            return '' 
        except Exception:
            self.log.error('Exception raise in do_request')
            return ''

        msgtype = wx_xml.get_wxmsg(msg, 'MsgType')
        to_user = wx_xml.get_wxmsg(msg, 'ToUserName')
        from_user = wx_xml.get_wxmsg(msg, 'FromUserName')
        if to_user != self.conf.id:
            self.log.error('to_user is err,in:%s,xml:%s' % (to_user, self.conf.id))
            return ''

        try:
            ret_text = self.process_msg(msg, msgtype, to_user, from_user)
        except IException as ie:
            ie.detail()
            return wx_xml.reply_text_msg(from_user, to_user, wx_xml.DEF_RESULT)
        return ret_text

    def process_encode(self, args, body):
        try:
            enctype = args['encrypt_type'][0]
            nonce = args['nonce'][0]
            timestamp = args['timestamp'][0]
            signature = args['signature'][0]
            msg_signature = args['msg_signature'][0]
        except KeyError:
            self.log.error('lack argus')
            return self.reply('', nonce)

        if enctype != self.ENCODE_AES:
            self.log.error('encode type is not aes, %s %s' % (enctype, self.ENCODE_AES))
            return self.reply('', nonce)

        if not self.check_signature(signature, timestamp, nonce, self.conf.token):
            self.log.error('check signature failed')
            return self.reply('', nonce)

        print 'check signature ok'
        doc = self.decode_xml(body, msg_signature, timestamp, nonce)
        if doc is None:
            self.log.error('decode request body failed')
            return self.reply('', nonce)

        try:
            msg = wx_xml.wxxml2dict(doc)
        except IException as e:
            e.detail()
            return self.reply('', nonce)
        except Exception:
            self.log.error('Exception raise in do_request')
            return self.reply('', nonce)

        msgtype = wx_xml.get_wxmsg(msg, 'MsgType')
        to_user = wx_xml.get_wxmsg(msg, 'ToUserName')
        from_user = wx_xml.get_wxmsg(msg, 'FromUserName')
        if to_user != self.conf.id:
            self.log.error('to_user is err,in:%s,xml:%s' % (to_user, self.conf.id))
            return self.reply('', nonce)

        try:
            to_xml = self.process_msg(msg, msgtype, to_user, from_user)
        except IException as ie:
            ie.detail()
            return self.reply('', nonce)
        return self.reply(to_xml, nonce)

    def process_msg(self, msg, msgtype, to_user, from_user):
        if msgtype == 'event':
            type, doc = self.eprocessor.process_event(msg, to_user, from_user)
            return self.do_doc(to_user, from_user, type, doc)
        elif msgtype == 'text':
            type, doc = self.mprocessor.process_text(msg, to_user, from_user)
            return self.do_doc(to_user, from_user, type, doc)
        elif msgtype == 'image':
            doc = self.mprocessor.process_image(msg, to_user, from_user)
            return wx_xml.reply_text_msg(from_user, to_user, doc)
        elif msgtype == 'voice':
            doc = self.mprocessor.process_voice(msg, to_user, from_user)
            return wx_xml.reply_text_msg(from_user, to_user, doc)
        elif msgtype == 'video':
            doc = self.mprocessor.process_video(msg, to_user, from_user)
            return wx_xml.reply_text_msg(from_user, to_user, doc)
        elif msgtype == 'location':
            doc = self.mprocessor.process_location(msg, to_user, from_user)
            return wx_xml.reply_text_msg(from_user, to_user, doc)
        elif msgtype == 'link':
            doc = self.mprocessor.process_link(msg, to_user, from_user)
            return wx_xml.reply_text_msg(from_user, to_user, doc)
        else:
            self.log.error('msgtype is unknown, %s' % msgtype)
            return wx_xml.reply_text_msg(from_user, to_user, wx_xml.DEF_RESULT)

    def do_doc(self, to_user, from_user, type, doc):
        if type == wx_xml.MsgType.FORMAT:
            return doc
        elif type == wx_xml.MsgType.TEXT:
            return wx_xml.reply_text_msg(from_user, to_user, doc)
        elif type == wx_xml.MsgType.IMAGE:
            return wx_xml.reply_image_msg(from_user, to_user, doc)
        elif type == wx_xml.MsgType.NEWS:
            return wx_xml.reply_news_msg(from_user, to_user, doc)
        elif type == wx_xml.MsgType.VOICE:
            return wx_xml.reply_voice_msg(from_user, to_user, doc)
        else:
            return wx_xml.reply_text_msg(from_user, to_user, wx_xml.DEF_RESULT)

    """
    Check whether the HTTP request is from WeChat 
    by verifying the signature. 
    """
    def check_signature(self, signature, timestamp, nonce, token):
        tmplist = [token, timestamp, nonce]
        tmplist.sort()
        tmpstr = "%s%s%s" % tuple(tmplist)
        hashstr = hashlib.sha1(tmpstr).hexdigest()
        if hashstr == signature:
            return True
        else:
            print hashstr, signature
            return False

    def decode_xml(self, body, msign, timestamp, nonce):
        ret, from_xml = self.wx_crypto.DecryptMsg(body, msign, timestamp, nonce)
        if ret != 0:
            return None
        else:
            return from_xml

    def encode_xml(self, to_xml, nonce, timestamp=None):
        ret, reply = self.wx_crypto.EncryptMsg(to_xml, nonce, timestamp)
        if ret != 0:
            return None
        else:
            return reply

    def reply(self, text, nonce=None):
        if nonce is None:
            to_nonce = self.DEF_NONCE
        else:
            to_nonce = nonce
        return self.encode_xml(text, nonce)

#if __name__ == '__main__':
#    LOG().setlogger('./log')
#    log = LOG().getlogger()
#    log.error('ssss')

