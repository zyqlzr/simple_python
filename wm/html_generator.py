#!/usr/bin/python
# -*- coding=utf-8 -*-

from pyh import *
import html_const
import html_js
from comm.err import ErrCode
from comm.err import IException
from menu_mgn import MenuMgn

class HtmlGenerator(object):
    def generate_menu_page_path(self, path=None):
        menus = MenuMgn().week_now
        for daymenu in menus:
            day = int(daymenu)
            if day < 1 or day > 7:
                print 'weekday num is invalid'
                continue
            html_path = path + '/wm_pay_' + daymenu + '.html'
            print '*****menu_path*****:\n',html_path,'\n*****menu*****:\n',menus[daymenu]
            page = self.generate_menu_single_page(week_menu=menus[daymenu])
            page.printOut(html_path)

    def generate_menu_outoftime(self, day_menu=[]):
        page = self.generate_menu_single_page(week_menu=day_menu, timeout=True)
        return page.printString()

    def generate_menu_page(self, day_menu=[]):
        page = self.generate_menu_single_page(week_menu=day_menu)
        return page.printString()

    def generate_menu_single_page(self, week_menu=[], timeout=False):
        page = PyH(html_const.WM_ORDER_FANYOYO)
        page << meta(charset='utf-8')
        page << meta(name="viewport", content="width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no")
        page.addJS(html_const.WX_CORE_JS)
        page.addCSS(html_const.WX_BASE_CSS)
        page.addCSS(html_const.WX_WM_CSS)
        if timeout is True:
            self.generate_menu_title(page, timeout)
            self.generate_timeout(page)
        else:
            self.generate_menu_title(page)
        self.generate_menu_dinner(page, week_menu, timeout)
        page << script(html_js.order_js, type='text/javascript')
        return page

    def generate_timeout(self, page=None):
        div_to = div(cl="timeout")
        span_to = span(html_const.WM_ORDER_TIME)
        #img_to = img(src=html_const.WM_TIMEOUT_IMG)
        #div_to << img_to
        div_to << span_to
        page << div_to

    def generate_menu_title(self, page=None, timeout=False):
        div_title = div(cl="menu-title")
        div_inner_title = div()
        span_title = span(html_const.WM_MENU_TS, cl="menu-name")
        i_title = i(cl="menu-flag up")
        div_inner_title << span_title
        div_inner_title << i_title
        div_title << div_inner_title
        page << div_title

        if timeout is True:
            div_titles = div(cl="menu-titles hide")
        else:
            div_titles = div(cl="menu-titles")
        div_menu_ts = div(html_const.WM_MENU_TS, cl="ts highlight")
        div_menu_ts.addData(type=0)
        div_menu_xc = div(html_const.WM_MENU_XC, cl="xc")
        div_menu_xc.addData(type=1)
        div_menu_yl = div(html_const.WM_MENU_YL, cl="yl")
        div_menu_yl.addData(type=2)
        div_titles << div_menu_ts
        div_titles << div_menu_xc
        div_titles << div_menu_yl
        page << div_titles

    def generate_menu_dinner(self, page=None, week_menu=[], timeout=False):
        if page is None or 0 == len(week_menu):
            print 'page none or week_menu empty'
            return

        div_base = 'fyy-dinner-'
        arr = []
        for i in [0, 1, 2]:
            div_name = div_base + str(i)
            if i > 0:
                div_name += ' hide'
            div_tmp = div(cl=div_name)
            arr.append(div_tmp)

        for ele in week_menu:
            type = 0
            if ('type' in ele and 0 <= ele['type'] and 
                ele['type'] <= 2):
                type = ele['type']
            self.generate_menu_section(arr[type], ele, timeout)
        for div_ele in arr:
            page << div_ele
        page << br()
        page << br()
        page << br()
        self.generate_menu_submit(page)

    def generate_menu_section(self, div_dinner=None, ele=None, timeout=False):
        if div_dinner is None or ele is None:
            return False 

        if ('id' not in ele or 'price' not in ele or 
            'title' not in ele or 'discount' not in ele or 
            'max' not in ele or 'purl' not in ele or 'des' not in ele):
            return False 
        section_menu = section(cl='fyy-tt')

        div_s_menu = div(cl='fyy-tt-c')
        div_m_img = div(cl='m-img')
        div_m_img << img(src=ele['purl'])

        div_m_title = div(cl='m-title')
        span_m = span(ele['title'])
        menu_price = html_const.WM_ORDER_MONEY + str(ele['price'])
        strong_m = strong(menu_price)
        div_m_title << span_m
        div_m_title << strong_m  

        div_m_text = div(cl='m-text')
        p_text = p(ele['des'])
        div_m_text << p_text

        div_s_menu << div_m_img
        div_s_menu << div_m_title
        div_s_menu << div_m_text

        if timeout is False:
            div_s_sel = div(cl='fyy-tt-sel')
            span_min = span(cl='minus')
            b_min = b()
            span_min << b_min
            span_info = span('0', cl='num')
            span_info.addData(price=ele['price'], food=ele['id'], 
                title=ele['title'], discount=ele['discount']) 
            span_plus = span(cl='plus')
            b_plus = b()
            span_plus << b_plus
            div_s_sel << span_min
            div_s_sel << span_info
            div_s_sel << span_plus
            div_tips = div(cl='fyy-tt-tips hide')
        else:
            div_s_sel = div(cl='fyy-tt-sel hide')
            div_tips = div(cl='fyy-tt-tips')
            div_tips << span(html_const.WM_ORDER_FINISH)

        section_menu << div_s_menu
        section_menu << div_s_sel
        section_menu << div_tips
        div_dinner << section_menu

    def generate_menu_submit(self, page):
        div_submit = div(cl='fyy-submit')
        zero_count = '0' + html_const.WM_ORDER_FEN
        zero_money = '0.00' + html_const.WM_ORDER_YUAN
        strong_sel = strong(zero_count, id='count')
        span_sel = span(html_const.WM_ORDER_ALLSEL, cl='all-sel')
        span_sel << strong_sel
        strong_money = strong(zero_money, id='money_num')
        span_money = span(html_const.WM_ORDER_ALLCOUNT, cl='all-money')
        span_money << strong_money
        span_submit = span(cl='checkmark', id='submit')
        div_submit << span_sel
        div_submit << span_money
        div_submit << span_submit
        page << div_submit

    def generate_order_page(self, order_arr=[]):
        if 0 == len(order_arr):
            return self.generate_order_empty()
        page = PyH(html_const.WM_ORDER_LIST_TITLE)
        page << meta(charset='utf-8')
        page << meta(name="viewport", content="width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no")
        page.addJS(html_const.WX_CORE_JS)
        page.addCSS(html_const.WX_BASE_CSS)
        page.addCSS(html_const.WX_WM_CSS)
        self.generate_order_all(page, order_arr)
        return page.printString()

    def generate_order_header(self, page=None):
        header_order = header(cl='order-header')
        h1_order = h1(html_const.WM_ORDER_LIST_TITLE)
        header_order << h1_order
        page << header_order

    def generate_order_empty(self, page=None):
        page = PyH(html_const.WM_ORDER_LIST_TITLE)
        page << meta(charset='utf-8')
        page << meta(name="viewport", content="width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no")
        page.addJS(html_const.WX_CORE_JS)
        page.addCSS(html_const.WX_BASE_CSS)
	page.addCSS(html_const.WX_WMEMPTY_CSS)
        page.addBody(cl='order-empty')
        page << p(html_const.WM_ORDER_EMPTY)
        return page.printString()

    def generate_order_all(self, page=None, ele_arr=None):
        if page is None:
            return
        div_all = div(cl='order-all')
        print ele_arr
        for ele in ele_arr:
            if ele is None or '_id' not in ele or 'p' not in ele:
                continue
            date = ele['_id'].split(':')[0]
            price = ele['p']
            menu = ele['menu']
            print menu
            if 0 == len(menu):
                return
            div_order = div(cl='fyy-order')
            p_detail = p(cl='order-info')
            p_detail << span(date)
            p_detail << strong(str(price) + html_const.WM_ORDER_YUAN)
            ul_list = ul(cl='order-list')
            for ele in menu:
                li_menu = li(cl='order-e');
                if 'n' not in ele or 't' not in ele:
                    continue
                title = ele['t']
                num = str(ele['n']) + html_const.WM_ORDER_FEN
                li_menu << span(title)
                li_menu << strong(num)
                ul_list << li_menu
            div_order << p_detail
            div_order << ul_list
            div_all << div_order
        page << div_all

    def generate_page(self, openid=None, info={}, discount={}):
        if openid is None:
            raise IException(ErrCode.ParamErr, 'input err')

        page = PyH(html_const.WM_ORDER_TITLE)
        page << meta(charset='utf-8')
        page << meta(name="viewport", content="width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no")
        page.addCSS(html_const.WX_BASE_CSS)
        page.addCSS(html_const.WX_WM_CSS)
        page.addJS(html_const.WX_CORE_JS)

        page << div(cl='hide') << span(openid, cl='fyy-openid hide')#, data-id='openid')
        self.page_discount_add(page, discount)
        display = self.page_info_add(page, info)
        self.page_addr_add(page, display)
        self.page_order_add(page, display)

        self.page_address_add(page)
        page << br()
        page << br()
        page << br()
        page << div(cl='fyy-submit') << span(cl='submit checkmark')
        page << script(html_js.submit_js, type='text/javascript')
        return page.printString()

    def page_discount_add(self, page=None, discount={}):
        if (page is None or 'type' not in discount or 
            'price' not in discount or 'title' not in discount):
            raise IException(ErrCode.ParamErr, 'input err')
        div_dc = div(cl='discount hide')
        div_dc.addData(type=discount['type'], price=discount['price'], 
            title=discount['title']) 
        page << div_dc

    def page_info_add(self, page=None, info={}):
        if page is None:
            raise IException(ErrCode.ParamErr, 'page null')

        if info is not None and 'lastest_info' in info and len(info['lastest_info']) > 0:
            div_info = div(cl='fyy-info')
            div_info << p(html_const.WM_ORDER_PERSON, cl='info-person')
            ul_addr = ul(cl='info-addr')
            ul_addr << li(html_const.WM_ORDER_ADDR, cl='info-title')
            ul_phone = ul(cl='info-phone')
            ul_phone << li(html_const.WM_ORDER_PHONE, cl='info-title')
            last_info = info['lastest_info']
            if 'addr' in last_info:
                ul_addr << li(last_info['addr'], cl='info-value')
            else:
                ul_addr << li(cl='info-value')

            if 'phone' in last_info:
                ul_phone << li(last_info['phone'], cl='info-value')
            else:
                ul_phone << li(cl='info-value')
            div_info << ul_addr
            div_info << ul_phone
            div_info << p(html_const.WM_ORDER_EDIT, cl='info-edit')
            page << div_info
            return True
        else:
            div_info = div(cl='fyy-info hide')
            div_info << p(html_const.WM_ORDER_PERSON, cl='info-person')
            ul_addr = ul(cl='info-addr')
            ul_addr << li(html_const.WM_ORDER_ADDR, cl='info-title')
            ul_phone = ul(cl='info-phone')
            ul_phone << li(html_const.WM_ORDER_PHONE, cl='info-title')
            ul_addr << li(cl='info-value')
            ul_phone << li(cl='info-value')
            div_info << ul_addr
            div_info << ul_phone
            div_info << p(html_const.WM_ORDER_EDIT, cl='info-edit')
            page << div_info
            return False

    def page_order_add(self, page=None, display=False):
        if page is None:
            raise IException(ErrCode.ParamErr, 'page null')
        if display is False:
            div_order = div(cl='fyy-order hide')
        else:
            div_order = div(cl='fyy-order')

        p_order = p(html_const.WM_ORDER_INFO, cl='order-info')
        ul_list = ul(cl='order-list')
        div_order << p_order
        div_order << ul_list
        page << div_order

    def page_addr_add(self, page=None, display=False):
        if page is None:
            raise IException(ErrCode.ParamErr, 'page null')

        if display is False:
            add_addr = div(cl='addr-add')
            add_addr_p = p() 
            add_addr_p << b()
            add_addr_p << strong(html_const.WM_ORDER_ADD)
            add_addr << add_addr_p
            page << add_addr
        else:
            add_addr = div(cl='addr-add hide')
            add_addr_p = p() 
            add_addr_p << b() << strong(html_const.WM_ORDER_ADD)
            add_addr << add_addr_p
            page << add_addr 

    def page_info_add_old(self, page=None, info={}):
        if page is None:
            raise IException(ErrCode.ParamErr, 'page null')
        div_info = None
        if 'lastest_info' in info and len(info['lastest_info']) > 0:
            div_info = div(cl='fyy-info')
            last_info = info['lastest_info']
            if 'addr' in last_info:
                div_info << span(last_info['addr'], cl='fyy-i-addr')
            else:
                div_info << span(cl='fyy-i-addr')

            if 'phone' in last_info:
                div_info << span(last_info['phone'], cl='fyy-i-tel')
            else:
                div_info << span(cl='fyy-i-tel')

            div_info << span(html_const.WX_ADDR_EDIT, cl='fyy-i-edit')
            page << div_info
            return True
        else:
            div_info = div(cl='fyy-info hide')
            div_info << span(cl='fyy-i-addr')
            div_info << span(cl='fyy-i-tel')
            div_info << span(html_const.WX_ADDR_EDIT, cl='fyy-i-edit')
            page << div_info
            return False

    def page_address_add(self, page=None):
        if page is None:
            raise IException(ErrCode.ParamErr, 'page null') 
        p_addr = p() << input(type='text', placeholder=html_const.WX_ATTR_ADDR, cl='input-addr', value="")
        p_phone = p() << input(type='text', placeholder=html_const.WX_ATTR_PHONE, cl='input-phone', value="")
        p_check = p(html_const.WX_ATTR_CHECK, cl='input-check')
        div_addr = div(cl='fyy-add hide')
        div_addr << p_addr
        div_addr << p_phone
        div_addr << p_check
        page << div_addr

def addr_page_test():
    openid = 'openid_value'
    info1 = {'lastest_info': {'phone':'18757571517', 'addr':'xuefulu'} }
    info2 = {'lastest_info': {}}
    info3 = {} 

    generate1 = HtmlGenerator()
    print generate1.generate_page(openid, info1)
    generate2 = HtmlGenerator()
    print generate2.generate_page(openid, info2)
    generate3 = HtmlGenerator()
    print generate3.generate_page(openid, info3)

def pay_page_test():
    menu_xml = './menu.xml'
    mmgn = MenuMgn()
    mmgn.load(menu_xml)
    generate_menu = HtmlGenerator() 
    generate_menu.generate_menu_page_path(path='./pay_html')

if __name__ == '__main__':
    pay_page_test()

