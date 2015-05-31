#!/usr/bin/python
# -*- coding=utf-8 -*-

CMD_HELP = """
  [列出admin成员命令 list all/admin/employee/client]
  [添加admin成员  add admin/employee/client wx_id]
  [删除admin成员 del wx wx_id]
  [删除admin成员 del name name_id]

  查询命令格式如下：
  [查询今日订阅 sub ]
  [查询昨日订阅 sub - ]
  [按时间查询定义 sub 2015-1-15]
  [查询取消订阅 unsub;格式类似sub ]

  [按编号查询订单 1 number ]
  [统计今日订单 1 a ]
  [统计昨日订单 1 a - ]
  [按日期统计 1 a 2015-5-25 ]
  
  [成为client的命令： fanyoyo 英文名字 ]
  [成为root的命令： root 英文名字]
  [重新加载所有页面： reload_url]
  [列出所有页面： page info]
  [列出某一个页面： page 页面名字]
"""

ROOT_HELP = """ROOT HELP
  查询命令格式如下：
  [查询今日订阅 sub ]
  [查询昨日订阅 sub - ]
  [按时间查询定义 sub 2015-1-15]
  [查询取消订阅 unsub;格式类似sub ]

  [按编号查询订单 1 number ]
  [统计今日订单 1 a ]
  [统计昨日订单 1 a - ]
  [按日期统计 1 a 2015-5-25 ]
"""

ADMIN_HELP = """Admin Help
  [按编号查询订单 1 number ]
  [统计今日订单 1 a ]
  [统计昨日订单 1 a - ]
  [按日期统计 1 a 2015-5-25 ]
"""

EMPLOYEE_HELP = """'EMPLOYEE Help'
  [按编号查询订单 1 number ]
  [统计今日订单 1 a ]
  [统计昨日订单 1 a - ]
  [按日期统计 1 a 2015-5-25 ]
"""

QUERY_NOTHING = """查询无结果
"""

CLIENT_CONGRATULATIONS = """恭喜您，
您可以使用如下命令查询：
  [按编号查询订单 1 number ]
  [统计今日订单 1 a ]
  [统计昨日订单 1 a - ]
  [按日期统计 1 a 2015-5-25 ]
"""

CLIENT_HELP = """CLIENT Help
  [按编号查询订单 1 number ]
  [统计今日订单 1 a ]
  [统计昨日订单 1 a - ]
  [按日期统计 1 a 2015-5-25 ]
"""

CLIENT_FORMAT = """CLIENT_HELP：
  fanyoyo 英文名字
"""

FANYOYO_NOTE = 'fanyoyo'

BACK_DOOR = """
   zyqlzr
"""

ORDER_NO_FIND = """找不到订单"""
ORDER_FORMAT = """订餐总数:%d\n:即点即送:%d\n:预约:%d\n总收入:%d\n菜品点餐清单:\n%s"""
ORDER_EMPTY = """订单为空"""
ORDER_MENU = """%s:%d份\n"""

ADDR_ORDER_FORMAT = """手机:%s\n地址:%s\n价格:%s\n订单:\n"""
ADDR_MENU_FORMAT = """%s %d 份\n"""

ORDER_MENU_FORMAT = """
编号: %d 
地址: %s
手机号: %s
总金额:%s
订单:%s
"""



MENU_FORMAT = """%s: %s元; 类型:%d"""


