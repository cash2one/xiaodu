#-*-coding:utf-8-*-
'''
Created on 2014-7-18
@author: wsx
'''
import datetime
import sys
import re
import traceback
import commands
import json
import os

f_path = os.path.dirname(__file__)                                                                                                                                                       
if len(f_path) < 1: f_path = "."
sys.path.append(f_path)
sys.path.append(f_path + "/..")

from dal.RedisDal import RedisDal
from dal.MySqlDal import pyMySQL
from conf.CommConfig import CommonObj
from conf.DBConfig import DBConfig
from bll.AttrDbBll import AttrDbBll

import sys
#set encode
reload(sys)
sys.setdefaultencoding("utf-8")

class WorkObj(object):
    def __init__(self):
        self.site = None
        self.work_type = None
        self.title = None
        self.list_link = None
        self.work_id = None
        self.episode = None
        self.link = None
        self.crawle_time = None
        self.commit_time = None
        
    def __str__(self):
        return ",".join([self.site, self.work_id, self.work_type, self.title, self.list_link, self.episode, self.link, self.commit_time, self.crawle_time])

class Log_ST(object):
    def __init__(self):
        self.new_work_dic = {}
        self.old_work_dic = {}
        self.new_work_json_dic = {}
        self.old_work_json_dic = {}
        self.__attrBll = None
        
    def __get_logTime(self, log_str):
        ret = True
        crawle_time = None
        log_time = re.search('\d{4}\-\d{2}\-\d{2}\s+\d{2}:\d{2}:\d{2}', log_str, re.I)
        if log_time is not None:
            crawle_time = log_time.group()
        else:
            ret = False
        return ret, crawle_time
    
    def load_NEW_WORK_NEW_OBJ_log_to_dic(self, file_name):
        ret = True
        self.new_work_dic.clear()
        try:
            with open(file_name, "r") as log_file:
                for line in log_file:
                    fd_list = line.split('\t')
                    if len(fd_list) >= 7:
                        #build
                        obj = WorkObj()
                        log_str = fd_list[0]
                        ret, obj.crawle_time = self.__get_logTime(log_str)
                        if not ret:
                            del obj
                            continue
                        obj.site = fd_list[1]
                        obj.work_type = fd_list[2]
                        obj.title = fd_list[3]
                        obj.list_link = fd_list[4]
                        obj.episode = fd_list[5]
                        obj.link = fd_list[6]
                        
                        #format
                        link = str(obj.link)
                        if link.endswith("\n"):
                            obj.link = link[:-1]
                        
                        #obj st
                        if obj.list_link not in self.new_work_dic:
                            self.new_work_dic[obj.list_link] = list()
                        self.new_work_dic[obj.list_link].append(obj)
        except:
            ret = False
            t, v, tb = sys.exc_info()
            print('load_NEW_WORK_NEW_OBJ_log_to_dic failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
        return ret
             
    def load_OLD_WORK_NEW_OBJ_log_to_dic(self, file_name):
        ret = True
        self.old_work_dic.clear()
        try:
            with open(file_name, "r") as log_file:
                for line in log_file:
                    fd_list = line.split('\t')
                    if len(fd_list) >= 8:
                        #build
                        obj = WorkObj()
                        log_str = fd_list[0]
                        ret, obj.crawle_time = self.__get_logTime(log_str)
                        if not ret:
                            del obj
                            continue
                        obj.site = fd_list[1]
                        obj.work_type = fd_list[2]
                        obj.work_id = fd_list[3]
                        obj.title = fd_list[4]
                        obj.list_link = fd_list[5]
                        obj.episode = fd_list[6]
                        obj.link = fd_list[7]
                        
                        #format
                        link = str(obj.link)
                        if link.endswith("\n"):
                            obj.link = link[:-1]
                        
                        #obj st
                        if obj.list_link not in self.old_work_dic:
                            self.old_work_dic[obj.list_link] = list()
                        self.old_work_dic[obj.list_link].append(obj)
        except:
            ret = False
            t, v, tb = sys.exc_info()
            print('load_OLD_WORK_NEW_OBJ_log_to_dic failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
        return ret
    
    def __get_obj_commit_time(self, work_type, list_link, episode):
        ret = -1
        try:
            #get time from db(mysql)
            if self.__attrBll is None:
                self.__attrBll = AttrDbBll()
                ret = self.__attrBll.initDBConfig()
                if not ret:
                    self.__attrBll = None
                    return -1
            ret = self.__attrBll.get_obj_commit_time(work_type, list_link, episode)
            if ret > 0:
                return datetime.datetime.fromtimestamp(ret).strftime('%Y-%m-%d %H:%M:%S')
        except:
            t, v, tb = sys.exc_info()
            print('load_OLD_WORK_NEW_OBJ_log_to_dic failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
        return ret
    
    def __trans_work_dic_json(self, work_dic, json_dic):
        json_dic['work_list'] = []
        for list_link, objlist in work_dic.iteritems():
            if len(objlist) > 0:
                work_temp_dic = {}
                work_temp_dic['work_title'] = objlist[0].title
                work_temp_dic['work_type'] = objlist[0].work_type
                work_temp_dic['work_id'] = objlist[0].work_id
                work_temp_dic['list_link'] = objlist[0].list_link
                work_temp_dic['obj_list'] = []
                for obj in objlist:
                    obj_temp_dic = {}
                    obj_temp_dic['obj_link'] =  obj.link
                    obj_temp_dic['obj_episode'] =  obj.episode
                    obj_temp_dic['obj_crawle_time'] =  obj.crawle_time
                    obj_temp_dic['obj_commit_time'] =  self.__get_obj_commit_time(obj.work_type, list_link, obj.episode)
                    work_temp_dic['obj_list'].append(obj_temp_dic)
                
                json_dic['work_list'].append(work_temp_dic)
       
    def trans_NEW_WORK_OBJ_to_json(self):
        ret = True
        dic_json = None
        try:
            self.new_work_json_dic.clear()
            self.new_work_json_dic['match_type'] = CommonObj.MONITOR_WORK_TYPE['NEW_WORK_OBJ']
            self.new_work_json_dic['work_num'] = len(self.new_work_dic)
            self.__trans_work_dic_json(self.new_work_dic, self.new_work_json_dic)
            dic_json = json.dumps(obj=self.new_work_json_dic, ensure_ascii=False)
        except:
            ret = False
            t, v, tb = sys.exc_info()
            print('trans_NEW_WORK_OBJ_to_json failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
        return ret, dic_json
    
    def trans_OLD_WORK_OBJ_to_json(self):
        ret = True
        dic_json = None
        try:
            self.old_work_json_dic.clear()
            self.old_work_json_dic['match_type'] = CommonObj.MONITOR_WORK_TYPE['OLD_WORK_OBJ']
            self.old_work_json_dic['work_num'] = len(self.old_work_dic)
            self.__trans_work_dic_json(self.old_work_dic, self.old_work_json_dic)
            dic_json = json.dumps(obj=self.old_work_json_dic, ensure_ascii=False)
        except:
            ret = False
            t, v, tb = sys.exc_info()
            print('trans_NEW_WORK_OBJ_to_json failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
        return ret, dic_json
    
    @staticmethod  
    def execute_cmd_with_boolen_return(cmd):
        f_cmd = "%s;echo $?"%(cmd)
        r = commands.getoutput(f_cmd)
        if(r=='0' or r=='1'):
            return True
        return False
                    

class LogSender(object):
    __collQueue = RedisDal()
    log_st = Log_ST()

    def __init__(self, startTime=datetime.datetime.now()):
        self.timeFormat = CommonObj.MONITOR_ST_PATH['ST_LOG_NAME_SUFFIX_FORMAT']
        self.lastTime = datetime.datetime.now().strftime(self.timeFormat)
        self.startTime = startTime - datetime.timedelta(days=1)
        
        self.st_log_path = CommonObj.MONITOR_ST_PATH['ST_LOG_PATH']
        if not self.st_log_path.endswith("/"):
            self.st_log_path = self.st_log_path + "/"
        self.st_log_file = self.st_log_path + CommonObj.MONITOR_ST_PATH['ST_LOG_NAME']
        
        self.new_work_new_obj_outputFile = self.st_log_path + "new_work_st.txt"
        self.old_work_new_obj_outputFile = self.st_log_path + "new_obj_st.txt"
        
        
    def __parseLog(self, inputFile):
        new_work_new_obj_cmd = " ".join(["fgrep 'NEW_WORK_NEW_OBJ'", inputFile, " > ", self.new_work_new_obj_outputFile])
        new_work_parse_ret = Log_ST.execute_cmd_with_boolen_return(new_work_new_obj_cmd)
        old_work_new_obj_cmd = " ".join(["fgrep 'OLD_WORK_NEW_OBJ'", inputFile, " > ", self.old_work_new_obj_outputFile])
        new_obj_parse_ret = Log_ST.execute_cmd_with_boolen_return(old_work_new_obj_cmd)
        return new_work_parse_ret, new_obj_parse_ret

    def __sendInfo(self):
        if self.log_st.load_NEW_WORK_NEW_OBJ_log_to_dic(self.new_work_new_obj_outputFile):
            ret, new_work_json = self.log_st.trans_NEW_WORK_OBJ_to_json()
            if ret:
                print 'new work json: ', new_work_json
                #send new_work to server
                self.__collQueue.monitorlist_push(CommonObj.MONITOR_CONF['MONITOR_QUEUE_NAME'], new_work_json)
                
        else:
            print 'load_NEW_WORK_NEW_OBJ_log_to_dic failed!!!'
        
        if self.log_st.load_OLD_WORK_NEW_OBJ_log_to_dic(self.old_work_new_obj_outputFile):
            ret, old_work_json = self.log_st.trans_OLD_WORK_OBJ_to_json()
            if ret:
                print 'old_work_json', old_work_json
                #send new_obj to server
                self.__collQueue.monitorlist_push(CommonObj.MONITOR_CONF['MONITOR_QUEUE_NAME'], old_work_json)
        else:
            print 'load_OLD_WORK_NEW_OBJ_log_to_dic failed!!!'

    def loadInfoFromLog(self):
        try:
            thisTime = self.startTime.strftime(self.timeFormat)
            inputFile = self.st_log_file + CommonObj.MONITOR_ST_PATH['ST_LOG_NAME_CONN_MARK'] + thisTime
            new_work_parse_ret,new_obj_parse_ret = self.__parseLog(inputFile)
            if new_work_parse_ret and new_obj_parse_ret:
                self.__sendInfo()
            else:
                print 'parseLog failed!!! new_work_parse_ret=%s, new_obj_parse_ret=%s' %(new_work_parse_ret,new_obj_parse_ret)
            self.lastTime = self.startTime
        except:
            t, v, tb = sys.exc_info()
            print('loadInfoFromLog failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
            


        
if __name__ == '__main__':
    startTime = None
    sender = LogSender()
    sender.loadInfoFromLog()
