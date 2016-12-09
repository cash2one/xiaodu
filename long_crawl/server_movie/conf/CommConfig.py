#-*-coding:utf-8-*-
'''
Created on 2014-7-18
@author: wsx
'''

class CommonObj(object):
    TABLE_TYPE = {'DATA_ORI':'data_ori', 'OBJ_ORI':'obj_ori'}
    
    QUEUE_NAME = {'LINKLIST_QUEUE':'linklist_queue', 'CACHE_QUEUE':'cache_queue', 'DATAOBJ_QUEUE':'dataobj_queue', 'MONITOR_QUEUE':'monitor_queue'}
    
    WORK_TYPE = {'TV':'tvplay', 'SHOW':'show', 'COMIC':'comic', 'MOVIE':'movie'}
    
    POBJ_FAILED_REASON = {'EPNO_ERR':' the episode is not exist or exception', 'IMG_ERR':'the horiz_img is not exist or exception', "OTHER_ERR":'except cur'}
    
    LOG_CONF = {'LOG_PATH':'./log', 'LOG_NAME':'attrdbopt'}

    OPT_THREAD_NUM = {'TV':5, 'SHOW':5, 'COMIC':5, 'MOVIE':10}

    MONITOR_CONF = {'MONITOR_TURN_ON':False, 'MONITOR_QUEUE_NAME':'monInfo'}

    MONITOR_ST_PATH = {'ST_LOG_PATH':'./log', 'ST_LOG_NAME':'attrdbopt.log.wf', 'ST_LOG_NAME_CONN_MARK':'.', 'ST_LOG_NAME_SUFFIX_FORMAT':'%Y-%m-%d'} 
        
    MONITOR_WORK_TYPE = {'NEW_WORK_OBJ':1,  'OLD_WORK_OBJ':0}
