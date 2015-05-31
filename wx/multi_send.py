#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
from wx_mongo import WxMongo
from comm import url_rsp 
from comm import api_const

ACCESS_CACHE_TOKEN = 'access_token'

def send_to_admin(text=None, openid=None, mongo=None):
    cache_token = mongo.cache.get_key(ACCESS_CACHE_TOKEN)
    if 'value' not in cache_token:
        return
    token = cache_token['value']
    url = api_const.WXUrl.SERVICE_URL % token
    msg = {}
    msg['touser'] = openid
    msg['msgtype'] = 'text'
    msg['text'] = {'content':text}
    msg_data = json.dumps(msg, ensure_ascii=False).encode('utf-8')
    ret = url_rsp.send_url_request(url, post=msg_data)
    return ret 
