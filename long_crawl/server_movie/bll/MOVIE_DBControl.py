#-*-coding:utf-8-*-
'''
Created on 2014-7-18
@author: wsx
'''

import os
import sys
import traceback
import threading
import json
import signal
import time

f_path = os.path.dirname(__file__)                                                                                                                                                       
if len(f_path) < 1: f_path = "."
sys.path.append(f_path)
sys.path.append(f_path + "/..")

from utils.LogUtil import Logger
from bll.AttrDbBll import AttrDbBll
from dal.RedisDal import RedisDal
from conf.CommConfig import CommonObj

import sys
#set encode
reload(sys)
sys.setdefaultencoding("utf-8")

class InitialInfo(object):
    def __init__(self):
        self.__attrBll = AttrDbBll()
        self.__queueBll = RedisDal()
    
    #init linklist queue
    def init_linkList_queue(self):
        for work_type in CommonObj.WORK_TYPE.values():
            ret, data = self.__attrBll.getAllListlinkInAttr(work_type)
            if ret:
                for row in data:
                    site = row[0]
                    link = row[1]
                    value = site + "$$" + link
                    self.__queueBll.linklist_push(work_type, value)

class AttrDBUpdateThread(threading.Thread):
    __logger = Logger.get_logger()

    def __init__(self, work_type):
        threading.Thread.__init__(self, name="AttrDBUpdateThread")
        self.__work_type = work_type
        self.__running = True
        self.__attrBll = None
        self.__queueBll = None
        
    def run(self):
        if self.__attrBll is None:
            self.__attrBll = AttrDbBll()
            ret = self.__attrBll.initDBConfig()
            if not ret:
                AttrDBUpdateThread.__logger.warning('initDBConfig failed in AttrDbBll')
                return 
        if self.__queueBll is None:
            self.__queueBll = RedisDal()
        cache_obj_list = list()
        json_data = ""
        while self.__running:
            #read redis and get json_data
            try:
                data = self.__queueBll.objlist_pop(self.__work_type)
                json_data = data[1]
                if json_data is not None and len(json_data)>0:
                    try:
                        #parse json str
                        json_obj = json.loads(json_data)
                    except:
                        #format json str
                        data = json_data.decode('gbk').encode('utf-8')
                        json_obj = json.loads(data)
                    #update attr db
                    update_cache = self.__attrBll.updateAttrData(json_obj, cache_obj_list)
                    #update redis
                    if update_cache:
                        site = json_obj['site']
                        work_type = json_obj['work_type']
                        queue_key = site + "$" + work_type
                        for obj in cache_obj_list:
                            url = obj['link']
                            no = str(obj['episode'])
                            value = url + "$$" + no
                            if 'payment' in obj:
                                payment = int(obj['payment'])
                                if payment != 0:
                                    value = value + "$$" + str(payment)
                            self.__queueBll.cache_push(queue_key, value)

            except Exception as e:
                t, v, tb = sys.exc_info()
                AttrDBUpdateThread.__logger.warning('parse json from queue failed, data=%s, json_data=%s, errmsg=%s,%s,%s' % (data, json_data, t, v, traceback.format_tb(tb)))
                        
    def stop(self):
        self.__running = False
  

if __name__ == '__main__':
    thr_lst = list()
    for index in range(0,5):
        movie_updater = AttrDBUpdateThread(CommonObj.WORK_TYPE['MOVIE'])
        thr_lst.append(movie_updater)

    for thr in thr_lst:
        thr.start()
