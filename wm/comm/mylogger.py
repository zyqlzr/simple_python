#!/usr/bin/python
#coding: utf-8

import logging
import logging.handlers
import os
import singleton

   
@singleton.singleton
class MyLogger(object):
    __LOG_FORMATER = '<%(levelname)s> %(asctime)s (%(process)d, %(thread)d) [%(module)s.%(funcName)s:%(lineno)d] %(message)s'

    def __init__(self):
        self.logname = ''
        self.logger = None

    def setlogger(self, logname):
        """ Set a logger, log files is divided into day-hours. """
        self.logname = logname
        logger = logging.getLogger(self.logname)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(self.__LOG_FORMATER)
        # If log path not exists, create dir
        logs_dir = os.path.join(os.path.curdir, "logs")
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        BACKUP_COUNT = 100
        file_time_handler = logging.handlers.TimedRotatingFileHandler(os.path.join(logs_dir, self.logname), "H", 1, BACKUP_COUNT)
        file_time_handler.suffix = "%Y%m%d%H.log"  # filename.suffix      
        file_time_handler.setFormatter(formatter)
        file_time_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_time_handler)
        self.logger = logger
        
    def getlogger(self):
        """ Get logger. """
        return self.logger

if __name__ == '__main__':
    MyLogger().setlogger('./log')
    MyLogger().getlogger().error('sssss') 
