#-*-coding:utf-8-*-
'''
Created on 2014-7-18
@author: wsx
'''

import os
import logging.handlers

from conf.CommConfig import CommonObj

class Logger(object):
    __logger = None

    def __init__(self):
        pass
    
    @staticmethod
    def __init_log(log_path, level=logging.INFO, when="D", backup=7,
             format="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s",
             datefmt="%Y-%m-%d %H:%M:%S"):
        formatter = logging.Formatter(format, datefmt)
        logger = logging.getLogger()
        logger.setLevel(level)
        
        log_dir = os.path.dirname(log_path)
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        
        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log",
                                                            when=when,
                                                            backupCount=backup)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log.wf",
                                                            when=when,
                                                            backupCount=backup)
        handler.setLevel(logging.WARNING)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger

    @staticmethod
    def get_logger():
        if Logger.__logger is None:
            log_path = CommonObj.LOG_CONF['LOG_PATH']
            log_name = CommonObj.LOG_CONF['LOG_NAME']
            if not log_path.endswith("/"):
                log_path = log_path + "/"
            log_path = log_path + log_name
            Logger.__logger = Logger.__init_log(log_path)
        return Logger.__logger
