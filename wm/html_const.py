#!/usr/bin/python
# -*- coding=utf-8 -*-

WX_ACCESS_TOKEN = 'access_token'

WX_ADDR_USE = '''使用'''
WX_ADDR_EDIT = '''编辑'''
WX_ADDR_DEL = '''删除'''

WX_ATTR_ADDR = '''地址'''
WX_ATTR_PHONE = '''手机'''
WX_ATTR_CHECK = '''地址确认'''

WX_BASE_CSS = 'http://www.fanyoyo.cn/css/base.css'
WX_WM_CSS = 'http://www.fanyoyo.cn/css/fyy_wm_mod.css'
WX_WMEMPTY_CSS = 'http://www.fanyoyo.cn/css/fyy_wm_empty.css'
WX_CORE_JS = 'http://www.fanyoyo.cn/js/core.js'

WM_ORDER_FANYOYO = """饭优悠"""
WM_ORDER_LIST_TITLE = """我的订单"""
WM_ORDER_TITLE = """订餐"""

WM_ORDER_ADD = """添加新地址"""
WM_ORDER_PERSON = """个人信息"""
WM_ORDER_ADDR = """送餐地址: """
WM_ORDER_PHONE = """手机号码: """
WM_ORDER_EDIT = """点击编辑信息"""
WM_ORDER_INFO = """订单详情"""

WM_ORDER_FEN = """份"""

WM_ORDER_YUAN = """元"""

WM_ORDER_EMPTY= """还没有订单，赶快下订单吧！"""

WM_ORDER_HEADER= """订餐：9:00-23:00"""

WM_ORDER_MONEY = """￥"""

WM_ORDER_ALLSEL = """已选："""

WM_ORDER_ALLCOUNT="""总计："""

WM_MENU_TS = """特色"""
WM_MENU_XC = """小炒"""
WM_MENU_YL = """饮料"""

WM_IMG_DISPLAY = """"""

WM_ORDER_TIME = """订餐时间6:00-21:00"""
WM_TIMEOUT_IMG = """"""
WM_ORDER_FINISH = """今日订餐结束"""

ORDER_PROTO = """
{
  'id':openid,
  'menu': { 
    menu_id: {
        'num': menu_num,
        'title' : name
    },

    menu_id: {
        'num': menu_num,
        'title' : name
    }
  },

  'user_info': [
    {
      'type': 0/1/2  add/mod/del
      'addr' : detail address,
      'phone' : phone number
    }
  ],

  'price': xxxxx
}
"""



