#!/usr/bin/python
# -*- coding=utf-8 -*-

from model import stat
from unit import mongo_test

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    #mongo_test.db_test()
    #mongo_test.singleton_test()
    #mongo_test.handler_test()
    #mongo_test.time_test()
    #mongo_test.stat_test()
    #mongo_test.user_test()
    mongo_test.admin_logic_test()

