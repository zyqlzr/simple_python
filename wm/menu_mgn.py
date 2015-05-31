#!/usr/bin/python
# -*- coding=utf-8 -*-

from xml.etree import ElementTree
import string
from comm import singleton
from comm.err import ErrCode
from comm.err import IException
import wx_mongo

@singleton.singleton
class MenuMgn(object):
    week_now = {'1':[],'2':[],'3':[], '4':[], '5':[], '6':[], '7':[]}
    week_time = {'1':[],'2':[],'3':[], '4':[], '5':[], '6':[], '7':[]}
    menu_now = {'1':[],'2':[],'3':[], '4':[], '5':[], '6':[], '7':[]}
    menu_time = {'1':[],'2':[],'3':[], '4':[], '5':[], '6':[], '7':[]}
    menus = {}
    path = ''
    def load(self, path=None):
        if path is None or not isinstance(path, basestring):
            info = 'menu.xml path is invalid'
            raise IException(ErrCode.ParamErr, info)
        self.path = path
        print self.path

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

        node_menu = tree.find('Menus')
        self.load_menu(node_menu)

        node_now = tree.find('Now')
        self.load_now(node_now)

        node_time = tree.find('Time')
        self.load_time(node_time)

    def load_menu(self, node=None):
        if node is None:
            raise IException(ErrCode.ParamErr, 'input invalid')
        menus = node.findall('menu')
        for item in menus:
            ele = {}
            id = item.get('id')
            price = item.get('price')
            title = item.get('title')
            max = item.get('max')
            type = item.get('type')
            purl = item.get('purl')
            des = item.get('des')
            if (id is None or price is None or title is None or 
                max is None or purl is None or des is None):
                raise IException(ErrCode.ParamErr, 'input is invalid')
            ele['id'] = id
            ele['price'] = price
            ele['title'] = title
            ele['max'] = int(max)
            ele['type'] = int(type)
            ele['purl'] = purl
            ele['des'] = des
            if id not in self.menus:
                self.menus[id] = ele
            else:
                raise IException(ErrCode.ParamErr, 'menu repeated')
        print 'load menu'
        print self.menus

    def load_now(self, node=None):
        if node is None:
            raise IException(ErrCode.ParamErr, 'input invalid')
        self.now_discount = node.get('discount')
        week = node.findall('week')
        for day in week:
            day_num = day.get('num')
            day_menu = day.get('list').split(',')
            if int(day_num) < 1 or int(day_num) > 7:
                raise IException(ErrCode.ParamErr, 'day value invalid')
            if day_num not in self.week_now:
                raise IException(ErrCode.ParamErr, 'day invalid')
            self.menu_now[day_num] = day_menu
        print 'load now'
        print self.menu_now

    def load_time(self, node=None):
        if node is None:
            raise IException(ErrCode.ParamErr, 'input invalid')
        self.time_discount = node.get('discount')
        week = node.findall('week')
        for day in week:
            day_num = day.get('num')
            day_menu = day.get('list').split(',')
            if int(day_num) < 1 or int(day_num) > 7:
                raise IException(ErrCode.ParamErr, 'day value invalid')
            if day_num not in self.week_time:
                raise IException(ErrCode.ParamErr, 'day invalid')
            self.menu_time[day_num] = day_menu
        print 'load time'
        print self.menu_time

    def update(self):
        self.mongo = wx_mongo.WxMongo()
        self.update_stuff()
        self.update_menus()
        self.update_now()
        self.update_time()

    def update_stuff(self):
        for now_i in self.menu_now:
            day_num = int(now_i)
            if (day_num < 1 or day_num > 7):
                raise IException(ErrCode.ParamErr, 'day is invalid')
            day_menu = self.menu_now[now_i]
            for m in day_menu:
                if m not in self.menus:
                    raise IException(ErrCode.ParamErr, 'menu not defined')
                tmp_ele = self.menus[m]
                tmp = {}
                tmp['id'] = tmp_ele['id']
                tmp['price'] = tmp_ele['price']
                tmp['title'] = tmp_ele['title']
                tmp['max'] = tmp_ele['max']
                tmp['type'] = tmp_ele['type']
                tmp['purl'] = tmp_ele['purl']
                tmp['des'] = tmp_ele['des']
                tmp['discount'] = self.now_discount
                self.week_now[now_i].append(tmp)

        for time_i in self.menu_time:
            day_num = int(time_i)
            if (day_num < 1 or day_num > 7):
                raise IException(ErrCode.ParamErr, 'day is invalid')
            day_menu = self.menu_time[time_i]
            for m in day_menu:
                if m not in self.menus:
                    raise IException(ErrCode.ParamErr, 'menu not defined')
                tmp_ele = self.menus[m]
                tmp = {}
                tmp['id'] = tmp_ele['id']
                tmp['price'] = tmp_ele['price']
                tmp['title'] = tmp_ele['title']
                tmp['max'] = tmp_ele['max']
                tmp['type'] = tmp_ele['type']
                tmp['purl'] = tmp_ele['purl']
                tmp['des'] = tmp_ele['des']
                tmp['discount'] = self.time_discount
                self.week_time[time_i].append(tmp)

    def update_now(self):
        for day in self.week_now:
            day_num = int(day)
            if day_num < 1 or day_num > 7:
                print 'weekday num is invalid,',day
                continue
            self.update_menu_now(day, self.week_now[day])

    def update_time(self):
        for day in self.week_now:
            day_num = int(day)
            if day_num < 1 or day_num > 7:
                print 'weekday num is invalid,',day
                continue
            self.update_menu_time(day, self.week_time[day])

    def update_menus(self):
        for m in self.menus:
            menu = self.menus[m]
            if ('id' not in menu or 'price' not in menu or 
                'title' not in menu or 'max' not in menu or 
                'type' not in menu or 'purl' not in menu):
                print 'menu lack field'
                continue
            self.mongo.menu.update_menu(id=menu['id'], 
                price=menu['price'], title=menu['title'], 
                type=int(menu['type']), purl=menu['purl'], 
                max=menu['max'], des=menu['des'])

    def update_menu_now(self, day, menus=[]):
        mids = self.mongo.week_now.get_weekids(day)
        if mids is None or 'menu_id_arr' not in mids:
            self.mongo.week_now.update_weekmenu(day, menus, self.menu_now[day])
            return
        ids = self.menu_now[day] + mids['menu_id_arr']
        new_ids = list(set(ids))
        new_menus = []
        for i in new_ids:
            tmp = self.mongo.menu.get_menu(i)
            if tmp is None:
                print 'can not find menu ',i
                continue
            menu_ele = {}
            menu_ele['id'] = tmp['_id']
            menu_ele['price'] = tmp['price']
            menu_ele['title'] = tmp['title']
            menu_ele['type'] = tmp['type']
            menu_ele['purl'] = tmp['purl']
            menu_ele['max'] = tmp['max']
            menu_ele['des'] = tmp['des']
            menu_ele['discount'] = self.now_discount
            new_menus.append(menu_ele)
        print '****now_update:', day, '****\n', new_menus, new_ids
        self.mongo.week_now.update_weekmenu(day, new_menus, new_ids)

    def update_menu_time(self, day, menus={}):
        mids = self.mongo.week_time.get_weekids(day)
        if mids is None or 'menu_id_arr' not in mids:
            self.mongo.week_time.update_weektime(day, menus, self.menu_time[day])
            return
        ids = self.menu_time[day] + mids['menu_id_arr']
        new_ids = list(set(ids))
        new_menus = []
        for i in new_ids:
            tmp = self.mongo.menu.get_menu(i)
            if tmp is None:
                print 'can not find menu ',i
                continue
            menu_ele = {}
            menu_ele['id'] = tmp['_id']
            menu_ele['price'] = tmp['price']
            menu_ele['title'] = tmp['title']
            menu_ele['type'] = tmp['type']
            menu_ele['purl'] = tmp['purl']
            menu_ele['max'] = tmp['max']
            menu_ele['des'] = tmp['des']
            menu_ele['discount'] = self.time_discount
            new_menus.append(menu_ele)
        print '****time_update:', day, '****\n', new_menus, new_ids
        self.mongo.week_time.update_weektime(day, new_menus, new_ids)

    def remove_menu(self):
        self.mongo = wx_mongo.WxMongo()
        self.remove_now()
        self.remove_time()

    def remove_now(self):
        for day in self.menu_now:
            day_menu = self.menu_now[day]
            menu_num = len(day_menu)
            if 0 == menu_num:
                continue
            mids = self.mongo.week_now.get_weekids(day)
            if mids is None or 'menu_id_arr' not in mids:
                continue
            ids = mids['menu_id_arr']
            print '**before del:**\n', ids, day_menu
            ids = self.remove_id(ids, day_menu)
            print '**after del:**\n', ids, day_menu
            menus = []
            for i in ids:
                tmp = self.mongo.menu.get_menu(i)
                if tmp is None:
                    print 'can not find menu ',i
                    continue
                menu_ele = {}
                menu_ele['id'] = tmp['_id']
                menu_ele['price'] = tmp['price']
                menu_ele['title'] = tmp['title']
                menu_ele['type'] = tmp['type']
                menu_ele['purl'] = tmp['purl']
                menu_ele['max'] = tmp['max']
                menu_ele['des'] = tmp['des']
                menu_ele['discount'] = self.now_discount
                menus.append(menu_ele)
            print '***now_remove:', day, '***\n', menus, ids
            self.mongo.week_now.update_weekmenu(day, menus, ids)

    def remove_time(self):
        for day in self.menu_time:
            day_menu = self.menu_time[day]
            menu_num = len(day_menu)
            if 0 == menu_num:
                continue
            mids = self.mongo.week_time.get_weekids(day)
            if mids is None or 'menu_id_arr' not in mids:
                continue
            ids = mids['menu_id_arr']
            print '**before del:**\n', ids, day_menu
            ids = self.remove_id(ids, day_menu)
            print '**after del:**\n', ids, day_menu
            menus = []
            for i in ids:
                tmp = self.mongo.menu.get_menu(i)
                if tmp is None:
                    print 'can not find menu ',i
                    continue
                menu_ele = {}
                menu_ele['id'] = tmp['_id']
                menu_ele['price'] = tmp['price']
                menu_ele['title'] = tmp['title']
                menu_ele['type'] = tmp['type']
                menu_ele['purl'] = tmp['purl']
                menu_ele['max'] = tmp['max']
                menu_ele['des'] = tmp['des']
                menu_ele['discount'] = self.time_discount
                menus.append(menu_ele)
            print '***time_remove:', day, '***\n', menus, ids
            self.mongo.week_time.update_weektime(day, menus, ids)

    def remove_id(self, a=[], b=[]):
        ok = []
        for i in a:
            find = False
            for j in b:
                if i == j:
                    find = True
            if find is False:
                ok.append(i)
        return ok

if __name__ == '__main__':
    menu_xml = './menu.xml'
    mmgn = MenuMgn()
    mmgn.load(menu_xml)
    print '***week_now***:\n',mmgn.week_now
    print '***week_time***:\n',mmgn.week_time

