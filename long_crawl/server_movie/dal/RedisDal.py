#-*-coding:utf-8-*-
'''
Created on 2014-7-18
@author: wsx
'''

import redis

from utils.LogUtil import Logger
from conf.CommConfig import CommonObj
from conf.DBConfig import DBConfig

class RedisDal(object):
    __logger = Logger.get_logger()

    def __init__(self):
        self.__db_handler_dic = {
                                 CommonObj.QUEUE_NAME['LINKLIST_QUEUE']:None,
                                 CommonObj.QUEUE_NAME['CACHE_QUEUE']:None,
                                 CommonObj.QUEUE_NAME['DATAOBJ_QUEUE']:None,
                                 CommonObj.QUEUE_NAME['MONITOR_QUEUE']:None
                                }
    def __del__(self):
        for conn in self.__db_handler_dic.values():
            if conn is not None:
                #wait for check
                #conn.disconnect()
                pass
        
    def __connect_to_redis(self, queue_name):
        try:
            if queue_name not in DBConfig.REDIS:
                return False
            if self.__db_handler_dic[queue_name] is None:
                self.__db_handler_dic[queue_name] = redis.StrictRedis(DBConfig.REDIS[queue_name]['host'],
                                                                      DBConfig.REDIS[queue_name]['port'],
                                                                      DBConfig.REDIS[queue_name]['db'])            
                RedisDal.__logger.debug('Connect to Redis Server success, host=%s, port=%d, db=%d' \
                                    % (DBConfig.REDIS[queue_name]['host'], DBConfig.REDIS[queue_name]['port'], DBConfig.REDIS[queue_name]['db']))
            return True 
        except Exception, e:
            RedisDal.__logger.warning('Connect to Redis Server Failed, host=%s, port=%d, db=%d, errmsg=%s' \
                                    % (DBConfig.REDIS[queue_name]['host'], DBConfig.REDIS[queue_name]['port'], DBConfig.REDIS[queue_name]['db'], e))
            return False
        
    #LISTLIST_QUEUE operator
    def linklist_push(self, list_name, value, head=False):
        queue_name = CommonObj.QUEUE_NAME['LINKLIST_QUEUE']
        if self.__db_handler_dic[queue_name] is None:
            if not self.__connect_to_redis(queue_name):
                return None
        if head:
            return self.__db_handler_dic[queue_name].lpush(list_name, value)
        else:
            return self.__db_handler_dic[queue_name].rpush(list_name, value)
            
    def linklist_pop(self, list_name, head=True):
        queue_name = CommonObj.QUEUE_NAME['LINKLIST_QUEUE']
        if self.__db_handler_dic[queue_name] is None:
            if not self.__connect_to_redis(queue_name):
                return None
        if head:
            return self.__db_handler_dic[queue_name].lpop(list_name)
        else:
            return self.__db_handler_dic[queue_name].rpop(list_name)   
            
    def linklist_size(self, list_name): 
        queue_name = CommonObj.QUEUE_NAME['LINKLIST_QUEUE']
        if self.__db_handler_dic[queue_name] is None:
            if not self.__connect_to_redis(queue_name):
                return None 
        return self.__db_handler_dic[queue_name].llen(list_name)
    #CACHE_QUEUE operator
    def cache_push(self, set_name, value):
        queue_name = CommonObj.QUEUE_NAME['CACHE_QUEUE']
        if self.__db_handler_dic[queue_name] is None:
            if not self.__connect_to_redis(queue_name):
                return None 
        return self.__db_handler_dic[queue_name].sadd(set_name, value)
    
    def cache_exist(self, set_name, value):
        queue_name = CommonObj.QUEUE_NAME['CACHE_QUEUE']
        if self.__db_handler_dic[queue_name] is None:
            if not self.__connect_to_redis(queue_name):
                return None 
        return self.__db_handler_dic[queue_name].sismember(set_name, value)
    
    #DATAOBJ_QUEUE operator
    def objlist_push(self, list_name, value, head=False):
        queue_name = CommonObj.QUEUE_NAME['DATAOBJ_QUEUE']
        if self.__db_handler_dic[queue_name] is None:
            if not self.__connect_to_redis(queue_name):
                return None
        if head:
            return self.__db_handler_dic[queue_name].lpush(list_name, value)
        else:
            return self.__db_handler_dic[queue_name].rpush(list_name, value)
            
    def objlist_pop(self, list_name, head=True):
        queue_name = CommonObj.QUEUE_NAME['DATAOBJ_QUEUE']
        if self.__db_handler_dic[queue_name] is None:
            if not self.__connect_to_redis(queue_name):
                return None
        if head:
            return self.__db_handler_dic[queue_name].blpop(list_name)
        else:
            return self.__db_handler_dic[queue_name].brpop(list_name)   
            
    def objlist_size(self, list_name): 
        queue_name = CommonObj.QUEUE_NAME['DATAOBJ_QUEUE']
        if self.__db_handler_dic[queue_name] is None:
            if not self.__connect_to_redis(queue_name):
                return None 
        return self.__db_handler_dic[queue_name].llen(list_name)

    #MONITOR_QUEUE operator
    def monitorlist_push(self, list_name, value, head=False):
        queue_name = CommonObj.QUEUE_NAME['MONITOR_QUEUE']
        if self.__db_handler_dic[queue_name] is None:
            if not self.__connect_to_redis(queue_name):
                return None
        if head:
            return self.__db_handler_dic[queue_name].lpush(list_name, value)
        else:
            return self.__db_handler_dic[queue_name].rpush(list_name, value)
            
    def monitorlist_pop(self, list_name, head=True):
        queue_name = CommonObj.QUEUE_NAME['MONITOR_QUEUE']
        if self.__db_handler_dic[queue_name] is None:
            if not self.__connect_to_redis(queue_name):
                return None
        if head:
            return self.__db_handler_dic[queue_name].lpop(list_name)
        else:
            return self.__db_handler_dic[queue_name].rpop(list_name)   
            
    def monitorlist_size(self, list_name): 
        queue_name = CommonObj.QUEUE_NAME['MONITOR_QUEUE']
        if self.__db_handler_dic[queue_name] is None:
            if not self.__connect_to_redis(queue_name):
                return None 
        return self.__db_handler_dic[queue_name].llen(list_name)
