#!/usr/bin/python
# -*- coding=utf-8 -*-

from xml.etree import ElementTree
import string
from comm import singleton
from comm.err import ErrCode
from comm.err import IException
import wx_xml

'''page item = 
{
  'title':"xxxxx", 
  'description': "xxxxx",
  'url': "http://xxxxx",
  'picurl': "http://xxxxx"
}'''

WELCOME_KEY = 'welcome'
HOMEPAGE_KEY = 'homepage'
RECOMMAND_KEY = 'recommend'
WMRECOMMAND_KEY = 'wm-recommand'
DELICIOUS_KEY = 'delicious'

@singleton.singleton
class UrlMgr(object):
    def __init__(self):
        self.path = None 
        self.log = None
        self.welcome = []
        self.home_page = []
        self.recommand = []
        self.wm_recommand = []
        self.delicious = []
        self.pages = {}
        self.multi_pages = {}

    def init(self, path, log):
        self.path = path
        self.log = log
        self.load()

    def load(self):
        print self.path
        tree = None
        try:
            with open(self.path, 'rt') as f:
                tree = ElementTree.parse(f)
        except IOError:
            io_info = 'open %s failed' % self.path
            raise IException(ErrCode.ThirdErr, io_info)

        if tree is None:
            cinfo = 'parse xml %s failed' % self.path
            raise IException(ErrCode.ConfigErr, cinfo)

        all_node = tree.find('Pages')
        self.load_pages(all_node)

        view_node = tree.find('PageView')
        self.load_pageviews(view_node)

    def load_pages(self, node=None):
        self.pages = self.load_keyelement(node)

    def load_pageviews(self, node=None):
        if node is None:
            raise IException(ErrCode.ConfigErr, 'un-find pagesviews')
        sub_elements = node.findall('pageset')
        for item in sub_elements:
            key_name = item.get('name')
            if key_name == WELCOME_KEY:
                self.load_welcome(item)
                self.multi_pages[key_name] = self.welcome
            elif key_name == HOMEPAGE_KEY:
                self.load_homepage(item)
                self.multi_pages[key_name] = self.home_page
            elif key_name == RECOMMAND_KEY:
                self.load_recommand(item)
                self.multi_pages[key_name] = self.recommand
            elif key_name == WMRECOMMAND_KEY:
                self.load_wmrecommand(item)
                self.multi_pages[key_name] = self.wm_recommand
            elif key_name == DELICIOUS_KEY:
                self.load_delicious(item)
                self.multi_pages[key_name] = self.delicious
            else:
                tmp_arr = self.load_element(item)
                self.multi_pages[key_name] = tmp_arr

    def load_welcome(self, node=None):
        ele_arr = self.load_element(node)
        self.welcome = ele_arr

    def load_homepage(self, node=None):
        hp_arr = self.load_element(node)
        self.home_page = hp_arr

    def load_recommand(self, node):
        r_arr = self.load_element(node)
        self.recommand = r_arr

    def load_wmrecommand(self, node):
        wm_arr = self.load_element(node)
        self.wm_recommand = wm_arr

    def load_delicious(self, node):
        d_arr = self.load_element(node)
        self.delicious= d_arr

    def load_keyelement(self, node):
        if node is None:
            raise IException(ErrCode.ConfigErr, 'un-find xml_node')
        elements = {}
        sub_elements = node.findall('Item')
        for item in sub_elements:
            key = item.get('key')
            title = item.get('title')
            des = item.get('des')
            url = item.get('url')
            purl = item.get('pic_url')
            if (key is None or title is None or des is None or 
                url is None or purl is None):
                raise IException(ErrCode.ConfigErr, 'clickpage lack item')
            page_item = {}
            page_item['title'] = title
            page_item['description'] = des
            page_item['url'] = url
            page_item['picurl'] = purl
            #print page_item
            elements[key] = page_item
        return elements

    def load_element(self, node):
        if node is None:
            raise IException(ErrCode.ConfigErr, 'un-find elements')
        elements = []
        sub_elements = node.findall('page')
        for item in sub_elements:
            ele_key = item.get('key')
            if ele_key is None:
                raise IException(ErrCode.ConfigErr, 'page lack key')
            if ele_key in self.pages:
                elements.append(self.pages[ele_key])
        return elements

    def welcomepage(self):
        return self.welcome

    def homepage(self):
        return self.home_page

    def recommandpage(self):
        return self.recommand
 
    def wmrecommandpage(self):
        return self.wm_recommand

    def allpages(self):
        all_arr = []
        for item in self.pages:
            all_arr.append(self.pages[item])
        return all_arr

if __name__ == '__main__':
    log = None
    path = './url.xml'
    url_mgr = UrlMgr()
    url_mgr.init(path, log)

    print "***homepage*** : ", url_mgr.home_page
    print "***welcome*** : ", url_mgr.welcome
    print "***recommand*** : ", url_mgr.recommand
    print "***wm-recommand*** : ", url_mgr.wm_recommand
    print "***all-pages*** : ", url_mgr.pages
    #for page in url_mgr.home_page:
    #    print "page in home_page", page

    h_msg = wx_xml.reply_news_msg('touser', 'fromuser', url_mgr.homepage())
    w_msg = wx_xml.reply_news_msg('touser', 'fromuser', url_mgr.welcomepage())
    r_msg = wx_xml.reply_news_msg('touser', 'fromuser', url_mgr.recommandpage())
    print h_msg.encode('utf-8')
    print w_msg.encode('utf-8')
    print r_msg.encode('utf-8')

    print url_mgr.multi_pages


