#-*-coding:utf-8-*-
'''
Created on 2014-7-18
@author: wsx
'''

import threading
import os
import sys
import traceback

from utils.LogUtil import Logger
from conf.CommConfig import CommonObj

class MonitorObj(object):
    def __init__(self, link, episode, monitorInfo=None):
        self.link = link
        self.episode = episode
        self.monitorInfo = monitorInfo

class LinklistInfo(object):
    def __init__(self):
        self.__title_dic = dict()
        self.__newobj_dic = dict()
        self.__oldobj_dic = dict()
        self.__failedobj_dic = dict()
        
    def __add_new_linklist(self, linklist, title):
        self.__title_dic[linklist] = title
        self.__newobj_dic[linklist] = list()
        self.__oldobj_dic[linklist] = list()
        self.__failedobj_dic[linklist] = list()
    
    def __exist_linklist(self, linklist):
        return linklist in self.__title_dic
    
    def is_empty(self):
        if len(self.__title_dic) <= 0:
            return True
        else:
            return False
        
    def incr_newobj_num(self, linklist, title):
        if not self.__exist_linklist(linklist):
            self.__add_new_linklist(linklist, title)
        self.__newobj_dic[linklist].append(1)
    
    def incr_oldobj_num(self, linklist, title):
        if not self.__exist_linklist(linklist):
            self.__add_new_linklist(linklist, title)
        self.__oldobj_dic[linklist].append(1)
        
    def incr_failedobj_num(self, linklist, title, monitorObj):
        if not self.__exist_linklist(linklist):
            self.__add_new_linklist(linklist, title)
        self.__failedobj_dic[linklist].append(monitorObj)

    def get_newojb_num(self, linklist):
        if linklist not in self.__newobj_dic:
            return 0
        return len(self.__newobj_dic[linklist])
    
    def get_oldojb_num(self, linklist):
        if linklist not in self.__oldobj_dic:
            return 0
        return len(self.__oldobj_dic[linklist])
    
    def get_failedobj_num(self, linklist):
        if linklist not in self.__failedobj_dic:
            return 0
        return len(self.__failedobj_dic[linklist])
    
    def report(self, file_handle):
        #format: linklist \t title \t newNum \t oldNum \t failedNum
        report_format = "\t{0}\t{1}\t{2}\t{3}\t{4}\n"
        for linklist, title in self.__title_dic.items():
            file_handle.write(report_format.format(linklist, title,
                                                   self.get_newojb_num(linklist), 
                                                   self.get_oldojb_num(linklist),
                                                   self.get_failedobj_num(linklist)))
    
class Monitor(object):
    __logger = Logger.get_logger()

    def __init__(self):
        self.site_dic = dict()
        self.lock = threading.Lock()

    def __build_site_monitor(self, site):
            self.site_dic = {
                         site:
                         {
                          CommonObj.WORK_TYPE['TV']:LinklistInfo(),
                          CommonObj.WORK_TYPE['SHOW']:LinklistInfo(),
                          CommonObj.WORK_TYPE['COMIC']:LinklistInfo(),
                          CommonObj.WORK_TYPE['MOVIE']:LinklistInfo()
                          }
                        }
        
    def addNewObj(self, site, work_type, linklist, title):
        self.lock.acquire()
        try:
            if site not in self.site_dic:
                self.__build_site_monitor(site)
            self.site_dic[site][work_type].incr_newobj_num(linklist, title)
        except:
            t, v, tb = sys.exc_info()
            Monitor.__logger.warning('addNewObj failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
        finally:
            self.lock.release()
    
    def addOldObj(self, site, work_type, linklist, title):
        self.lock.acquire()
        try:
            if site not in self.site_dic:
                self.__build_site_monitor(site)
            self.site_dic[site][work_type].incr_oldobj_num(linklist, title)
        except:
            t, v, tb = sys.exc_info()
            Monitor.__logger.warning('addOldObj failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
        finally:
            self.lock.release()

    def addFailObj(self, site, work_type, linklist, title, monitorObj):
        self.lock.acquire()
        try:
            if site not in self.site_dic:
                self.__build_site_monitor(site)
            self.site_dic[site][work_type].incr_failedobj_num(linklist, title, monitorObj)
        except:
            t, v, tb = sys.exc_info()
            Monitor.__logger.warning('addFailObj failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
        finally:
            self.lock.release()

    def resetMonitor(self):
        self.lock.acquire()
        self.site_dic = dict()
        self.lock.release()
    
    def reportInfo(self, report_filename):
        self.lock.acquire()
        path = "./report/"
        if not os.path.exists(path):
            os.mkdir(path)
        report_filename = path + report_filename
        try:
            with open(report_filename, "a+") as report_file:
                for site,linklist_dic in self.site_dic.items():
                    report_file.write("============" + site + "========\n")
                    for key, obj in linklist_dic.items():
                        report_file.write(key+":\n")
                        if not obj.is_empty():
                            obj.report(report_file)
                        else:
                            report_file.write('\tempety\n')
        except:
            t, v, tb = sys.exc_info()
            Monitor.__logger.warning('reportInfo failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
        finally:
            self.lock.release()

if __name__ == '__main__':
    monitor = Monitor()
    monitorObj = MonitorObj("link", "episode", CommonObj.POBJ_FAILED_REASON['EPNO_ERR'])
    monitor.addFailObj("qq.com", CommonObj.WORK_TYPE['MOVIE'], "xxx", "aaa", monitorObj)
    monitor.reportInfo('report')
