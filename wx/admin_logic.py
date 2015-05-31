#!/usr/bin/python
# -*- coding=utf-8 -*-

import time
import datetime
from comm import singleton
from wx_mongo import WxMongo
from comm.mylogger import MyLogger as LOG
from model import admin
import comm.mytime
import wx_xml
import url_mgr
import admin_const
import multi_send
"""
admin query format
"""

class CMD(object):
    LIST = 'list'
    ADD = 'add'
    DEL = 'del'
    UP = 'up'
    DOWN = 'down'
    CMDALL = 'cmd'
    RELOAD_URL = 'reload_url'
    CMD_INFO = 'cmd_info'
    PAGE = 'page'
    MENU = 'menu'
    SUB = 'sub'
    UNSUB = 'unsub'
    ORDER = 'order'
    AREA = 'area'
    ORDER_SIM = '1'
    AREA_SIM = '2'
    MENU_SIM = '3'

DEF_QUERY_NUM = 100

class AdminLogic(object):
    def __init__(self, mongo, logger):
        self.log = logger
        self.mongo = mongo

    def process_fanyoyo(self, wx_id=None, text=None):
        if wx_id is None or text is None:
            return wx_xml.MsgType.NEWS, url_mgr.UrlMgr().homepage()
        if -1 == text.find(admin_const.FANYOYO_NOTE):
            return wx_xml.MsgType.NEWS, url_mgr.UrlMgr().homepage()

        cmds = text.split(' ');
        cmd_num = len(cmds)
        if 2 != cmd_num or cmds[0] != admin_const.FANYOYO_NOTE:
            return wx_xml.MsgType.TEXT, admin_const.CLIENT_FORMAT

        exists = self.mongo.admin.find_name(cmds[1])
        if exists is not None:
            return wx_xml.MsgType.TEXT, admin_const.CLIENT_FORMAT 
        ret = self.mongo.admin.add_admin(wx_id, admin.PRI_CLIENT, cmds[1])
        if ret is None:
            return wx_xml.MsgType.TEXT, admin_const.CLIENT_FORMAT
        return wx_xml.MsgType.TEXT, admin_const.CLIENT_CONGRATULATIONS

    def process_text(self, wx_id, pri, text):
        if pri == admin.PRI_ROOT:
            return self.process_root(wx_id, text.split(' ')) 
        elif pri == admin.PRI_ADMIN:
            return wx_xml.MsgType.TEXT, self.process_admin(wx_id, text.split(' '))
        elif pri == admin.PRI_EMPLOYEE:
            return wx_xml.MsgType.TEXT, self.process_employee(wx_id, text.split(' '))
        elif pri == admin.PRI_CLIENT:
            return wx_xml.MsgType.TEXT, self.process_client(wx_id, text.split(' '))
        else:
            return wx_xml.MsgType.TEXT, "thank you"

    def process_admin(self, wx_id, cmd_arr):
        if (not isinstance(cmd_arr, list) 
            or 0 == len(cmd_arr)):
            return admin_const.ADMIN_HELP 
        cmd = cmd_arr[0]
        if cmd == CMD.ORDER_SIM:
            return self.process_order(wx_id, cmd_arr)
        else:
            return ADMIN_HELP

    def process_employee(self, wx_id, cmd_arr):
        if (not isinstance(cmd_arr, list) 
            or 0 == len(cmd_arr)):
            return admin_const.EMPLOYEE_HELP
        cmd = cmd_arr[0]
        if cmd == CMD.ORDER_SIM:
            return self.process_order(wx_id, cmd_arr)
        else:
            return admin_const.EMPLOYEE_HELP

    def process_client(self, wx_id, cmd_arr):
        cmd_num = len(cmd_arr)
        if cmd_arr[0] == CMD.EMPLOYEE_MENU:
            return admin_const.CLIENT_HELP
        elif cmd_arr[0] == CMD.EMPLOYEE_AREA:
            return admin_const.CLIENT_HELP
        elif cmd_arr[0] == 'root' and 2 == cmd_num:
            return self.process_backdoor(wx_id, cmd_arr)
        elif cmd == CMD.ORDER_SIM:
            return self.process_order(wx_id, cmd_arr)
        else:
            return admin_const.CLIENT_HELP

    def process_backdoor(self, wx_id, cmd_arr):
        if (cmd_arr[1] != 'zhengyang' and 
            cmd_arr[1] != 'jianglili' and 
            cmd_arr[1] != 'jiangzifa'):
            return admin_const.CLIENT_HELP
        roots = self.mongo.admin.find_name(cmd_arr[1])
        if roots is None:
            ret = self.mongo.admin.add_admin(wx_id, admin.PRI_ROOT, cmd_arr[1])
            if ret is None:
                return 'sorry, become root failed'
            return 'you are root'

        for i in roots:
            if i['pri'] == admin.PRI_ROOT:
                return 'root was existed' 

        ret = self.mongo.admin.update_admin(cmd_arr[1], admin.PRI_ROOT)
        if ret is None:
            return 'become root failed'
        return 'now, you are root'

    def process_root(self, wx_id, cmd_arr):
        if (not isinstance(cmd_arr, list) 
            or 0 == len(cmd_arr)):
            return admin_const.ROOT_HELP 
        cmd = cmd_arr[0]
        if cmd == CMD.LIST:
            return wx_xml.MsgType.TEXT, self.process_list(cmd_arr)
        elif cmd == CMD.ADD:
            return wx_xml.MsgType.TEXT, self.process_add(cmd_arr)
        elif cmd == CMD.DEL:
            return wx_xml.MsgType.TEXT, self.process_del(cmd_arr)
        elif cmd == CMD.UP:
            return wx_xml.MsgType.TEXT, self.process_up(cmd_arr)
        elif cmd == CMD.DOWN:
            return wx_xml.MsgType.TEXT, admin_const.ROOT_HELP
        elif cmd == CMD.RELOAD_URL:
            return self.process_reloadurl(cmd_arr)
        elif cmd == CMD.PAGE:
            return self.process_page(cmd_arr)
        elif cmd == CMD.SUB:
            return wx_xml.MsgType.TEXT, self.process_sub(cmd_arr)
        elif cmd == CMD.UNSUB:
            return wx_xml.MsgType.TEXT, self.process_unsub(cmd_arr)
        elif cmd == CMD.ORDER_SIM:
            return wx_xml.MsgType.TEXT, self.process_order(wx_id, cmd_arr)
        elif cmd == CMD.AREA_SIM:
            return wx_xml.MsgType.TEXT, self.process_menu(cmd_arr)
        else:
            return wx_xml.MsgType.TEXT, admin_const.ROOT_HELP

    def process_up(self, cmd_arr):
        cmd_num = len(cmd_arr)
        if cmd_num != 3:
            return admin_const.ROOT_HELP
        users = self.mongo.admin.find_name(cmd_arr[1])
        if users is None:
            return "can not find %s" % cmd_arr[1]

        if len(users) > 1:
            return "many people named %s" % cmd_arr[1]

        user_pri = admin.PRI_CLIENT
        if cmd_arr[2] == 'admin':
            user_pri = admin.PRI_ADMIN
        elif cmd_arr[2] == 'employee':
            user_pri = admin.PRI_EMPLOYEE
        else:
            return "pri of user is invalid"

        try:
            curr_pri = users[0]['pri']
        except Exception:
            return "system err, upgrade failed"
        
        ret = self.mongo.admin.update_admin(cmd_arr[1], user_pri)
        if ret is None:
            return 'upgrade failed'
        return 'upgrade %s to %s ok' % (cmd_arr[1], cmd_arr[2])

    def process_reloadurl(self, cmd_arr):
        cmd_num = len(cmd_arr)
        if cmd_num != 1:
            return admin_const.ROOT_HELP

        umgr = url_mgr.UrlMgr()
        umgr.load()
        page_arr = []

        for page in umgr.pages:
            page_arr.append(page)
        return wx_xml.MsgType.TEXT, self.list2str(page_arr)

    def process_page(self, cmd_arr):
        cmd_num = len(cmd_arr)
        if cmd_num != 2:
            return wx_xml.MsgType.TEXT, admin_const.ROOT_HELP

        pages = []
        umgr = url_mgr.UrlMgr()
        if cmd_arr[1] == 'info':
            for key in umgr.pages:
                pages.append(key)
            return wx_xml.MsgType.TEXT, self.list2str(pages)
        elif cmd_arr[1] == 'welcome':
            pages = umgr.welcomepage()
        elif cmd_arr[1] == 'homepage':
            pages = umgr.homepage()
        else:
            if cmd_arr[1] in umgr.pages:
                pages.append(umgr.pages[cmd_arr[1]])

        if 0 == len(pages):
            return wx_xml.MsgType.TEXT, admin_const.ROOT_HELP
        return wx_xml.MsgType.NEWS, pages

    def process_add(self, cmd_arr):
        cmd_num = len(cmd_arr)
        if cmd_num < 3:
            return admin_const.ROOT_HELP
        name = ''
        if cmd_num == 4:
            name = cmd_arr[3]

        admin_pri = cmd_arr[1]
        if admin_pri == 'admin':
            self.mongo.admin.add_admin(cmd_arr[2], admin.PRI_ADMIN, name)
            return 'ok'
        elif admin_pri == 'employee':
            self.mongo.admin.add_admin(cmd_arr[2], admin.PRI_EMPLOYEE, name)
            return 'ok'
        elif admin_pri == 'client':
            self.mongo.admin.add_admin(cmd_arr[2], admin.PRI_CLIENT, name)
            return 'ok'
        else:
            return admin_const.ROOT_HELP

    def process_del(self, cmd_arr):
        if len(cmd_arr) != 3:
            return admin_const.ROOT_HELP
        param1 = cmd_arr[1]
        param2 = cmd_arr[2]
        if param1 == 'wx':
            wx_del = self.mongo.admin.del_admin(user=param2)
            if wx_del is None:
                return 'can not find %s' % param2
            else:
                return 'ok'
        elif param1 == 'name':
            name_del = self.mongo.admin.del_admin(name=param2)
            if name_del is None:
                return 'can not find %s' % param2
            else:
                return 'ok' 
        else:
            name_del = self.mongo.admin.del_admin(user=param1, name=param2)
            if name_del is None:
                return 'can not find %s' % param2
            else:
                return 'ok' 

    def process_menu(self, cmd_arr):
        week_num = 0
        param_num = len(cmd_arr)
        if param_num < 2 or cmd_arr[1] != 'a':
            return 'cmd invalid'
        if param_num == 2:
            week_num = datetime.date.today().weekday() + 1
        else:
            third = cmd_arr[2]
            if third == '+':
                week_num = (datetime.date.today() + datetime.timedelta(days=1)).weekday() + 1
            elif third == '-':
                week_num = (datetime.date.today() - datetime.timedelta(days=1)).weekday() + 1
            else:
                week_num = int(third)
        weeks = self.mongo.week_now.get_weekmenu(str(week_num))
        if weeks is None or 'menu' not in weeks:
            return ''
        menus = weeks['menu']
        result_str = ''
        for menu in menus:
            result_str += admin_const.MENU_FORMAT % (menu['title'], menu['price'], menu['type'])
            result_str += '\n'
        return result_str

    def process_sub(self, cmd_arr):
        time = self.cmd2time(cmd_arr)
        self.log.debug('sub, time=%s,cmd=%s' % (time, str(cmd_arr)))
        if time is None:
            return ADMIN_HELP
        return self.list2str(self.mongo.stat.find_sub(time))

    def process_unsub(self, cmd_arr):
        self.log.debug('unsub, cmd=%s' % str(cmd_arr))
        time = self.cmd2time(cmd_arr)
        if time is None:
            return ADMIN_HELP
        return self.list2str(self.mongo.stat.find_unsub(time))

    def process_list(self, cmd_arr):
        param_num = len(cmd_arr)
        if param_num != 2:
            return admin_const.ROOT_HELP

        cmd_param = cmd_arr[1]
        if cmd_param == 'all':
            return self.list2str(self.mongo.admin.find_admin())
        elif cmd_param == 'admin':
            return self.list2str(self.mongo.admin.find_admin(admin.PRI_ADMIN))
        elif cmd_param == 'employee':
            return self.list2str(self.mongo.admin.find_admin(admin.PRI_EMPLOYEE))
        elif cmd_param == 'client':
            return self.list2str(self.mongo.admin.find_admin(admin.PRI_CLIENT))
        elif cmd_param == CMD.CMDALL:
            return admin_const.CMD_HELP
        else:
            return admin_const.ROOT_HELP

    def process_order(self, wx_id, cmd_arr):
        param_num = len(cmd_arr)
        if param_num < 2:
            return admin_const.ROOT_HELP

        cmd_param = cmd_arr[1]
        if cmd_param == 'a':
            return self.process_order_stat(cmd_arr)
        elif cmd_param == 'b':
            return self.process_order_addr(wx_id, cmd_arr)
        else:
            return self.process_order_query(cmd_param)

    def get_order_day(self, cmd_arr):
        param_num = len(cmd_arr)
        if param_num == 2:
            return comm.mytime.today2str()
        third = cmd_arr[2]
        if third == '+':
            return comm.mytime.tomorrow2str()
        elif third == '-':
            return comm.mytime.yesterday2str()
        else:
            return third

    def process_order_stat(self, cmd_arr):
        day = self.get_order_day(cmd_arr)
        arr = self.mongo.stat.find_order(day)
        arr_len = len(arr)
        if 0 == arr_len:
            return admin_const.ORDER_EMPTY
        count = {'oc': 0, 'nc': 0, 'tc': 0, 'pc': 0}
        menu_count = {}
        for o in arr:
            if o is None:
                continue
            self.get_single_order(o, count, menu_count)
        return self.convert_str(count, menu_count)

    def get_single_order(self, o=None, count={}, mcount={}):
        ele = self.mongo.order.get_order(o)
        if (ele is None or 'p' not in ele or 
            'menu' not in ele or 't' not in ele):
            print 'order lack field'
            return
        o_m = ele['menu']
        o_p = int(ele['p'])
        o_t = int(ele['t'])
        count['oc'] += 1
        if o_t == 0:
            count['nc'] += 1
        else:
            count['tc'] += 1
        count['pc'] += o_p

        print 'stat order_id:', o
        for menu in o_m:
            if ('m' not in menu or 'n' not in menu or 
                't' not in menu):
                print 'menu lack field'
                continue
            mid = menu['m']
            mnum = menu['n']
            mtitle = menu['t']
            if mid not in mcount:
                mcount[mid] = [mnum, mtitle]
            else:
                mcount[mid][0] += 1

    def convert_str(self, count, mcount):
        mstr = ''
        for mid in mcount:
            mstr += admin_const.ORDER_MENU % (mcount[mid][1], mcount[mid][0])
        return admin_const.ORDER_FORMAT % (count['oc'], count['nc'], count['tc'], count['pc'], mstr)

    def process_order_query(self, num=None):
        if num is None:
            return admin_const.ROOT_HELP
        oid = comm.mytime.today2str() + ':' + num
        order_ele = self.mongo.order.get_order(oid)
        if order_ele is None:
            return admin_const.ORDER_NO_FIND
        if ('oid' not in order_ele or 'p' not in order_ele or
            'menu' not in order_ele):
            print 'error, order lack field'
            return admin_const.ORDER_NO_FIND 
        order_user = self.mongo.user.find(order_ele['oid'])
        if order_user is None:
            print 'error, can not find user in order'
            return admin_const.ORDER_NO_FIND
        if ('lastest_info' not in order_user or 
            'phone' not in order_user['lastest_info'] or
            'addr' not in order_user['lastest_info']):
            print 'error, user address invalid'
            return admin_const.ORDER_NO_FIND
        address = order_user['lastest_info']
        u_phone = address['phone']
        u_addr = address['addr']
        menus = order_ele['menu']
        u_price = order_ele['p']
        result = admin_const.ORDER_MENU_FORMAT % (int(num), 
            u_phone, u_addr, u_price, self.menu2str(menus))
        return result

    def process_order_addr(self, wx_id, cmd_arr):
        day = self.get_order_day(cmd_arr)
        arr = self.mongo.stat.find_order(day)
        arr_len = len(arr)
        if 0 == arr_len:
            return admin_const.ORDER_EMPTY
        now_addr_orders = {}
        time_addr_orders = {}
        for o in arr:
            if o is None:
                continue
            self.get_single_addr(o, now_addr_orders, time_addr_orders)
        self.addr_stuff_send(wx_id, now_addr_orders)
        self.addr_stuff_send(wx_id, time_addr_orders)
        return 'ok'

    def addr_stuff_send(self, wx_id, addrs={}):
        buf = ''
        count = 0
        for ele in addrs:
            addr = addrs[ele]
            buf += admin_const.ADDR_ORDER_FORMAT % (addr['phone'], 
                addr['addr'], addr['price'])
            menus = addr['list']
            for menu in menus:
                buf += menu
            buf += '\n'
            if count >= 20:
                multi_send.send_to_admin(buf, wx_id, self.mongo)
                buf = ''
                count = 0
            else:
                count += 1
        if count > 0:
            multi_send.send_to_admin(buf, wx_id, self.mongo)

    def get_single_addr(self, o=None, now_addrs={}, time_addrs={}):
        print 'order_id:',o
        ele = self.mongo.order.get_order(o)
        if (ele is None or 'oid' not in ele or 
            'menu' not in ele or 't' not in ele or 'p' not in ele):
            print 'order lack field'
            return
        o_id = ele['oid']
        o_m = ele['menu']
        o_t = int(ele['t'])
        o_p = ele['p']
        print 'order_text=',ele
        if o_t == 0:
            self.get_now_addrs(o_id, o_m, o_p, now_addrs)
        else:
            self.get_time_addrs(o_id, o_m, o_p, time_addrs)

    def get_now_addrs(self, oid, menu, price, now_addrs={}):
        if oid not in now_addrs:
            ouser = self.mongo.user.find(oid)
            if (ouser is None or 'lastest_info' not in ouser or
                'phone' not in ouser['lastest_info'] or
                'addr' not in ouser['lastest_info']):
                return 
            address = ouser['lastest_info']
            u_phone = address['phone']
            u_addr = address['addr']
            now_addrs[oid] = {
                'phone': u_phone,
                'addr': u_addr,
                'price': price,
                'list': []
            }
        else:
            print 'type:',type(now_addrs[oid]['price']), now_addrs[oid]['price'], type(price), price
            now_addrs[oid]['price'] += price
        print 'total_price:', now_addrs[oid]['price']
        for i in menu:
            if ('n' not in i or 't' not in i):
                print 'menu lack field'
                continue
            tmp_str = admin_const.ADDR_MENU_FORMAT % (i['t'], i['n'])
            now_addrs[oid]['list'].append(tmp_str)

    def get_time_addrs(self, oid, menu, price, time_addrs={}):
        if oid not in time_addrs:
            ouser = self.mongo.user.find(oid)
            if (ouser is None or 'lastest_info' not in ouser or
                'phone' not in ouser['lastest_info'] or
                'addr' not in ouser['lastest_info']):
                return 
            address = order_user['lastest_info']
            u_phone = address['phone']
            u_addr = address['addr']
            time_addrs[oid] = {
                'phone': u_phone,
                'addr': u_addr,
                'price': price,
                'list': []
            }
        else:
            time_addrs[oid]['price'] += price
        for i in menu:
            if ('m' not in i or 'n' not in i or 't' not in i):
                print 'menu lack field'
                continue
            tmp_str = admin_const.ADDR_MENU_FORMAT % (menu['t'], menu['n'])
            time_addrs[oid]['list'].append(tmp_str)

    def menu2str(self, menu):
        menu_str = ''
        for i_menu in menu:
            if 'num' in i_menu and 'title' in i_menu:
                i_str = order_format.MENU_FORMAT % (i_menu['title'], i_menu['num'])
                menu_str += i_str
        return menu_str

    def cmd2time(self, cmd):
        cmd_num = len(cmd)
        if cmd_num == 0:
            return None
        if cmd_num == 1:
            return comm.mytime.today2str()

        param = cmd[1]
        if not isinstance(param, basestring):
            return None
        if param == '-':
            return comm.mytime.yesterday2str()
        elif param == '+':
            return comm.mytime.tomorrow2str()
        else:
            return param

    def cursor2str(self, cursor, num=DEF_QUERY_NUM):
        if cursor is None:
            return 'nothing'
        str = ''
        str += 'total number = %d' % cursor.count()
        for ele in cursor:
            str += '%s\n'
        return str

    def list2str(self, arr):
        if arr is None:
            return admin_const.QUERY_NOTHING
        str = 'total number = %d\n' % len(arr)
        count = 0 
        for ele in arr:
            if count > DEF_QUERY_NUM:
                break;
            str += '%s\n' % ele
            count += 1
        return str


