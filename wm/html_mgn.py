#!/usr/bin/python
# -*- coding=utf-8 -*-

import datetime
import time
from comm import singleton
from comm.err import ErrCode
from comm.err import IException
from html_generator import HtmlGenerator
import wx_mongo

@singleton.singleton
class html_mgn(object):
    def __init__(self):
        self.week = {}
        self.bnum = 0
        self.mongo = wx_mongo.WxMongo()

    def start(self, bnum=None):
        self.bnum = bnum

    def get_week_test(self, day):
        day_int = int(day)
        if day_int < 1 or day_int > 7:
            print 'day is invalid,',day
            return ''
        weeks = self.mongo.week_now.get_weekmenu(day)
        if weeks is None or 'menu' not in weeks:
	          return ''
        html = HtmlGenerator().generate_menu_page(weeks['menu'])
        return html

    def get_week_timeout(self):
        td = datetime.date.today()
        week_num = td.weekday()
        week_num += self.bnum
        weeks = self.mongo.week_now.get_weekmenu(str(week_num))
        if weeks is None or 'menu' not in weeks:
            return ''
        html = HtmlGenerator().generate_menu_outoftime(weeks['menu'])
        return html

    def get_week_now(self):
        td = datetime.date.today()
        week_num = td.weekday()
        week_num += self.bnum
        weeks = self.mongo.week_now.get_weekmenu(str(week_num))
        if weeks is None or 'menu' not in weeks:
            return ''
        html = HtmlGenerator().generate_menu_page(weeks['menu'])
        return html

    def get_week_time(self):
        td = datetime.date.today()
        week_num = td.weekday()
        week_num += self.bnum
        weeks = self.mongo.week_now.get_weektime(str(week_num))
        if 'menu' not in weeks:
            return ''
        html = HtmlGenerator().generate_menu_page(weeks['menu'])
        return html

    def load_week(self, path=None, pre=None, 
        suf=None, bnum=None):
        if (path is None or pre is None or 
            suf is None or bnum is None):
            raise IException(ErrCode.ParamErr, "input err")
        self.bnum = bnum
        week_loop = bnum
        print bnum
        while (week_loop < (bnum + 7)):
            apath = '%s/%s%d%s' % (path,pre,week_loop,suf)
            html_text = self.load_html(apath)
            self.week[week_loop] = html_text
            week_loop += 1
 
    def load_html(self, apath=None):
        if apath is None:
            raise IException(ErrCode.ParamErr, 'path not exist')
        try:
            with open(apath, 'r') as f:
                html_text = f.read()
        except IOError:
            io_info = 'open %s failed' % apath
            raise IException(ErrCode.ThirdErr, io_info)
        return html_text

    def today_menu(self):
        if 0 == len(self.week):
            return ''
        td = datetime.date.today()
        week_num = td.weekday()
        week_num += self.bnum
        if week_num in self.week:
            return self.week[week_num]
        return ''

    def display(self):
        for i in self.week:
            print 'file %s: %s' % (str(i), self.week[i])

if __name__ == '__main__':
    path = '/zy_data/running/resource/wm_html'
    pre = 'wm_nopay_'
    suf = '.html'
    bnum = 1
    html = html_mgn()    
    html.load_week(path, pre, suf, bnum)
    html.display()
    print 'get today menu:', html.today_menu()


