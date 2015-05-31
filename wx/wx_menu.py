#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

menu_fanyoyo_six = {
    'button' : [
	{
	    'name' : '外卖订餐',
	    'type' : 'view',
	    'url' : 'http://www.fanyoyo.cn/wm?menu=week'
	},
	{
	    'name' : 'YOYO美食',
		'sub_button' : [
		{
		    'name' : '店家推荐',
			'type' : 'click',
			'key'  : 'recommend'
		},
		{
		    'name' : '烤鱼鸡煲',
			'type' : 'click',
			'key' : 'huoguo'
		}, 
		{
		    'name' : '麻辣海鲜',
			'type' : 'click',
			'key' : 'spicy_seafood'
		},
		{
		    'name' : '天天特价',
			'type' : 'click',
			'key' : 'discount'
		}]
	},
	{
	    'name' : '饭优悠',
		'sub_button' : [
		{
		    'type' : 'click',
		    'name' : 'WIFI',
			'key' : 'wifi'
		},
		{
		    'type' : 'view',
			'name' : '我的订单',
			'url' : 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx3de96fc1838e3116&redirect_uri=http://www.fanyoyo.cn/shopping&response_type=code&scope=snsapi_base&state=1#wechat_redirect'
		},
		{
		    'type' : 'click',
		    'name' : '饭优悠*地址',
			'key' : 'position'
		},
		{
		    'type' : 'view',
			'name' : 'test',
			'url' : 'http://www.fanyoyo.cn/wm_html/test.html'
		}]
	}]
}

wx_curr_menu = menu_fanyoyo_six

if __name__ == '__main__':
    print menu_fanyoyo_six
    print 'json_uno:', json.dumps(menu_fanyoyo_six)
    print 'json_kkk:', json.dumps(menu_fanyoyo_six, ensure_ascii=False).encode('utf-8')
    print 'json_enc:', json.dumps(menu_fanyoyo_six).encode('utf-8')
    arr = menu_fanyoyo_five['button']
    dict = arr[0]
    print dict['name']

