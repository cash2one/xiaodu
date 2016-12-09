#-*-coding:utf-8-*-
'''
Created on 2014-7-18
@author: wsx
'''

import time
import types
import sys
import re
import traceback

#set encode
reload(sys)
sys.setdefaultencoding("utf-8")

import MySQLdb

from utils.LogUtil import Logger
from conf.CommConfig import CommonObj
from conf.DBConfig import DBConfig
from dal.MySqlDal import pyMySQL
from state.DBStateMonitor import Monitor
from state.DBStateMonitor import MonitorObj
from UtilityFunc import Funclib

class AttrDbBll(object):
    __logger = Logger.get_logger()
    db_config = DBConfig()
    monitor = Monitor()
    
    temp_st_data = {'OLD':0,'NEW':0}
    
    def __init__(self):
        self.__db_conn = None
        
    def initDBConfig(self):
        ret = True
        try:
            #host, user, passwd, dbname, port = '3306', char_set ='gbk' 
            self.__db_conn = pyMySQL(AttrDbBll.db_config.MYSQL['host'],
                                     AttrDbBll.db_config.MYSQL['uname'], 
                                     AttrDbBll.db_config.MYSQL['pwd'], 
                                     AttrDbBll.db_config.MYSQL['db_name'], 
                                     AttrDbBll.db_config.MYSQL['port'], 
                                     AttrDbBll.db_config.MYSQL['encoding'])
        except Exception as e:
            t, v, tb = sys.exc_info()
            AttrDbBll.__logger.warning('initDBConfig failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
            ret = False
            self.__db_conn = None
        return ret
    
    #table_type: 1:data_ori, 2:obj_ori
    def __getTableName(self, work_type, table_type):
        table_name = ""
        ret = True
        if table_type in CommonObj.TABLE_TYPE['DATA_ORI'] :
            if 'variety' in work_type or 'show' in work_type:
                table_name = 'shows_data_ori'
            elif 'tv' in work_type:
                table_name = 'tvplay_data_ori'
            elif 'comic' in work_type:
                table_name = 'comic_data_ori'
            elif 'movie' in work_type:
                table_name = 'movie_data_ori'
            else:
                ret = False
                AttrDbBll.__logger.warning('get tableName in __getTableName failed, work_type=%s, table_type=%s' % (work_type, table_type))
        elif table_type in CommonObj.TABLE_TYPE['OBJ_ORI'] :
            if 'variety' in work_type or 'show' in work_type:
                table_name = 'shows_obj_ori'
            elif 'tv' in work_type:
                table_name = 'tvplay_obj_ori'
            elif 'comic' in work_type:
                table_name = 'comic_obj_ori'
            else:
                ret = False
                AttrDbBll.__logger.warning('get tableName in __getTableName failed, work_type=%s, table_type=%s' % (work_type, table_type))
        else:
            ret = False
            AttrDbBll.__logger.warning('get tableName in __getTableName failed, work_type=%s, table_type=%s' % (work_type, table_type))
        return ret, table_name
    
    
    def __genObjSelectSql(self, work_type, list_link, episode):
        ret, table_name = self.__getTableName(work_type, CommonObj.TABLE_TYPE['OBJ_ORI'])
        select_sql = ""
        if ret:
            list_sign1, list_sign2 = Funclib.calc_url_sign(list_link)
            if list_sign1 == -1 or list_sign2 == -1:
                return False, '' 
            if 'variety' in work_type or 'show' in work_type:
                select_sql = "select flag_dead, insert_table_time, commit_type from %s where list_link_sign1 = '%s' and list_link_sign2 = '%s' and date = '%s'" % (table_name, list_sign1, list_sign2, episode)
            else:
                select_sql = "select flag_dead, insert_table_time, commit_type from %s where list_link_sign1 = '%s' and list_link_sign2 = '%s' and episode = '%s'" % (table_name, list_sign1, list_sign2, episode)
        return ret, select_sql

    def __genWorkTitleUpdateSql(self, work_type, sign1, sign2, title):
        ret, table_name = self.__getTableName(work_type, CommonObj.TABLE_TYPE['DATA_ORI'])
        update_sql = ""
        if ret:
            if type(title) is types.UnicodeType:
                title = title.encode('utf-8', "ignore")
            title = MySQLdb.escape_string(title)

            if 'movie' not in work_type:
                update_sql = "update %s set title = '%s' where sign1 = '%s' and sign2 = '%s'" % (table_name, title, sign1, sign2)
            else:
                update_sql = "update %s set title = '%s' where link_sign1 = '%s' link_sign2 = '%s'" % (table_name, title, sign1, sign2)
        return ret, update_sql
    
    def __genDataSelectSql(self, work_type, list_link):
        ret, table_name = self.__getTableName(work_type, CommonObj.TABLE_TYPE['DATA_ORI'])
        select_sql = ""
        if ret:
            #list_sign1, list_sign2 = Funclib.calc_url_sign(list_link)
            #if list_sign1 == -1 or list_sign2 == -1:
            #    return False, '' 
            if 'movie' not in work_type:
                #select_sql = "select site from %s where sign1 = '%s' and sign2 = '%s'" % (table_name, list_sign1, list_sign2)
                select_sql = "select list_link, sign1, sign2, base_id, state, is_delete from %s where normalized_list_link='%s'" %(table_name, list_link)
            else:
                #select_sql = "select site from %s where list_link_sign1 = '%s' and list_link_sign2 = '%s'" % (table_name, list_sign1, list_sign2)
                select_sql = "select link, link_sign1, link_sign2, base_id, state, is_delete from %s where normalized_link='%s'" %(table_name, list_link)
        return ret, select_sql
    
    
    def __genObjInsertSql(self, work_type, list_link, site, json_obj):
        insert_sql = ""
        sql_gbk = ""
        ret = True
        try:
            old_link = json_obj['link']
            new_link = Funclib.normalize_link_format(work_type, old_link)
            link_sign1, link_sign2 = Funclib.calc_url_sign(new_link)
            if link_sign1 == -1 or link_sign2 == -1:
                return False, '' 

            list_link_sign1, list_link_sign2 = Funclib.calc_url_sign(list_link)
            if list_link_sign1 == -1 or list_link_sign2 == -1:
                return False, '' 

            horizontal_img = json_obj['horiz_img']

            single_title = json_obj['single_title']
            if type(single_title) is types.UnicodeType:
                single_title = single_title.encode('utf-8', "ignore")
            single_title = MySQLdb.escape_string(single_title)

            duration_str = json_obj['duration']
            if type(duration_str) is types.StringType:
                if len(duration_str) <= 0:
                    duration = 0
                else:
                    duration = int(duration_str)
            else:
                duration = int(duration_str)

            guest = json_obj['guest']
            if type(guest) is types.UnicodeType:
                guest = guest.encode('utf-8', "ignore")
            guest = MySQLdb.escape_string(guest)

            ret, table_name = self.__getTableName(work_type, CommonObj.TABLE_TYPE['OBJ_ORI'])
            if ret:
                if 'variety' in work_type or 'show' in work_type:
                    cur_episode = json_obj['episode']
                    insert_sql = "insert into %s (guest, link, link_sign1, link_sign2, horizontal_img_url, single_title, date, duration, list_link, list_link_sign1, list_link_sign2, site, insert_table_time, update_table_time, commit_type) values('%s', '%s', %d, %d, '%s', '%s', '%s', %d, '%s', %d, %d, '%s', %d, %d, 1)" \
                           % (table_name, guest, new_link, link_sign1, link_sign2, horizontal_img, single_title, cur_episode, duration, list_link, list_link_sign1, list_link_sign2, site, int(time.time()), int(time.time()))
                elif 'tv' in work_type:
                    cur_episode = int(json_obj['episode'])
                    insert_sql = "insert into %s (link, link_sign1, link_sign2, horizontal_img_url, episode, duration, list_link, list_link_sign1, list_link_sign2, site, insert_table_time, update_table_time, commit_type) values('%s', %d, %d, '%s', %d, %d, '%s', %d, %d, '%s', %d, %d, 1)" \
                      % (table_name, new_link, link_sign1, link_sign2, horizontal_img, cur_episode, duration, list_link, list_link_sign1, list_link_sign2, site, int(time.time()), int(time.time()))
                elif 'comic' in work_type:
                    cur_episode = int(json_obj['episode'])
                    insert_sql = "insert into %s (link, link_sign1, link_sign2, horizontal_img_url, episode, duration, list_link, list_link_sign1, list_link_sign2, site, insert_table_time, update_table_time, commit_type) values('%s', %d, %d, '%s', %d, %d, '%s', %d, %d, '%s', %d, %d, 1)" \
                      % (table_name, new_link, link_sign1, link_sign2, horizontal_img, cur_episode, duration, list_link, list_link_sign1, list_link_sign2, site, int(time.time()), int(time.time()))
                else:
                    ret = False
            sql_gbk = insert_sql.decode('utf-8').encode('gbk', 'ignore')
        except Exception as e:
            ret = False
            t, v, tb = sys.exc_info()
            AttrDbBll.__logger.warning('genObjInsertSql failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
        return ret, sql_gbk
    

    def __genDataInsertSql(self, json_obj):
        insert_sql = ""
        sql_gbk = ""
        ret = True
        try:
            title = json_obj['title']
            if type(title) is types.UnicodeType:
                title = title.encode('utf-8', "ignore")
            title = MySQLdb.escape_string(title)

            site = json_obj['site']

            area = json_obj['area']
            if type(area) is types.UnicodeType:
                area = area.encode('utf-8', "ignore")
            area = MySQLdb.escape_string(area)

            language = json_obj['language']
            if type(language) is types.UnicodeType:
                language = language.encode('utf-8', "ignore")
            language = MySQLdb.escape_string(language)

            net_show_time = json_obj['net_show_time']

            intro = json_obj['intro']
            if type(intro) is types.UnicodeType:
                intro = intro.encode('utf-8', "ignore")
            intro = MySQLdb.escape_string(intro)

            verti_img = json_obj['verti_img']
            work_type = json_obj['work_type']

            list_link = json_obj['list_link']
            list_link_sign1, list_link_sign2 = Funclib.calc_url_sign(list_link)
            if list_link_sign1 == -1 or list_link_sign2 == -1:
                return False, '' 

            if 'movie' not in work_type:
                ret, table_name = self.__getTableName(work_type, CommonObj.TABLE_TYPE['DATA_ORI'])
                if ret:
                    insert_sql = "insert into %s (list_link, sign1, sign2, title, site, area, language, net_show_time, intro, vertical_img_url, insert_table_time, normalized_list_link) values('%s', %d, %d, '%s','%s','%s','%s','%s','%s','%s', %d, '%s')" \
                        %(table_name, list_link, list_link_sign1, list_link_sign2, title, site, area, language, net_show_time, intro, verti_img, int(time.time()), list_link)
            else:
                #movie: link==list_link
                table_name = 'movie_data_ori'
                obj = json_obj['obj_list'][0]
                ret, reason = self.__discardInfo(work_type, obj)
                if ret:
                    old_link = obj['link']
                    new_link = Funclib.normalize_link_format(work_type, old_link)
                    link_sign1,link_sign2 = Funclib.calc_url_sign(new_link)
                    if link_sign1 == -1 or link_sign2 == -1:
                        return False, '' 

                    title = obj['single_title']
                    if type(title) is types.UnicodeType:
                        title = title.encode('utf-8', "ignore")
                    title = MySQLdb.escape_string(title)

                    duration = int(obj['duration'])
                    horiz_img = obj['horiz_img']
                    insert_sql = "insert into %s (link, link_sign1, link_sign2, site, title,  area, duration, list_link, list_link_sign1, list_link_sign2, net_show_time, language, intro,  horizontal_img_url, vertical_img_url, insert_table_time, normalized_link, commit_type) values('%s', %d, %d, '%s', '%s', '%s', %d, '%s', %d, %d, '%s', '%s', '%s',  '%s', '%s', %d, '%s', 1)" \
                        %(table_name, new_link, link_sign1, link_sign2, site, title,  area, duration, list_link, list_link_sign1, list_link_sign2, net_show_time, language, intro, horiz_img, verti_img, int(time.time()), list_link) 

            sql_gbk = insert_sql.decode('utf-8').encode('gbk')
        except Exception as e:
            ret = False
            t, v, tb = sys.exc_info()
            AttrDbBll.__logger.warning('genDataInsertSql failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
        return ret, sql_gbk
    
    def __discardInfo(self, work_type, json_obj):
        ret = True
        reason = ""
        try:
            episode = json_obj['episode']
            if episode is not None:
                json_obj['episode'] = str(episode).strip()
                str_episode = json_obj['episode']
                if not re.match("^\d+$", str_episode):
                    AttrDbBll.__logger.warning('DISCARD OBJ FAILED:, episode is invalid, json=%s' %(json_obj))
                    return False, CommonObj.POBJ_FAILED_REASON['EPNO_ERR']
            else:
                AttrDbBll.__logger.warning('DISCARD OBJ FAILED:, episode is None, json=%s' %(json_obj))
                return False, CommonObj.POBJ_FAILED_REASON['EPNO_ERR']

            if 'variety' in work_type or 'show' in work_type:
                horiz_img = json_obj['horiz_img'].strip()
                episode = json_obj['episode'].strip()
                single_title = json_obj['single_title'].strip()
                if len(single_title) <= 0:
                    AttrDbBll.__logger.warning('DISCARD OBJ FAILED:, single_title is empty, json=%s' %(json_obj))
                    return False, CommonObj.POBJ_FAILED_REASON['EPNO_ERR']
                if len(horiz_img) <= 0: 
                    AttrDbBll.__logger.warning('DISCARD OBJ FAILED:, horiz_img is empty, json=%s' %(json_obj))
                    return False, CommonObj.POBJ_FAILED_REASON['EPNO_ERR']
                if len(episode)<=0:
                    AttrDbBll.__logger.warning('DISCARD OBJ FAILED:, episode is empty, json=%s' %(json_obj))
                    return False, CommonObj.POBJ_FAILED_REASON['IMG_ERR']
            elif 'tv' in work_type or 'comic' in work_type:
                episode = int(json_obj['episode'].strip())
                if episode<=0 or episode>2000:
                    AttrDbBll.__logger.warning('DISCARD OBJ FAILED:, episode is invalid, json=%s' %(json_obj))
                    return False, CommonObj.POBJ_FAILED_REASON['EPNO_ERR']
        except Exception as e:
            AttrDbBll.__logger.warning('discard OBJ infomation failed, emsg=%s, json=%s' %(e, json_obj))
            ret = False
            reason = CommonObj.POBJ_FAILED_REASON['OTHER_ERR']
        return ret, reason
    def getAllListlinkInAttr(self, work_type):
        data = None
        ret, table_name = self.__getTableName(work_type, CommonObj.TABLE_TYPE['DATA_ORI'])
        if ret:
            select_sql = "select site, list_link from %s" %(table_name)
            data = self.__db_conn.do_QUERY(select_sql)
        return ret, data

    def gen_report(self):
        sufix = time.strftime('%Y_%m_%d_%H_%M_%S')
        AttrDbBll.monitor.reportInfo("report_"+sufix)
        AttrDbBll.monitor.resetMonitor()

    def get_obj_commit_time(self, work_type, list_link, episode):
        ret = -1
        select_sql = ""
        table_name = ""
        try:
            if 'movie' not in work_type:
                sql_ret, select_sql = self.__genObjSelectSql(work_type, list_link, episode)
            else:
                table_name = self.__getTableName(work_type, CommonObj.TABLE_TYPE['DATA_ORI'])
                select_sql = "select flag_dead, insert_table_time, commit_type from %s where normalized_link='%s'" %(table_name, list_link)
            ret_data_rows = self.__db_conn.do_QUERY(select_sql)
            if ret_data_rows is not None:
                for row in ret_data_rows:
                    insert_table_time = int(row[1])
                    commit_type = int(row[2])
                    ret = insert_table_time
                    if commit_type == 0:
                        break
            else:
                AttrDbBll.__logger.warning("select obj_ori db failed, sql_cmd=%s" % (select_sql))
        except Exception as e:
            t, v, tb = sys.exc_info()
            AttrDbBll.__logger.warning('get_obj_commit_time failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
        return ret
    
    def report_num(self, work_type):
        file_name = work_type + "_rep.txt"
        with open(file_name, "a+") as repfile:
            repfile.write("new: " + str(AttrDbBll.temp_st_data['NEW']) + "\n")
            repfile.write("old: " + str(AttrDbBll.temp_st_data['OLD']) + "\n")
            #AttrDbBll.temp_st_data = {'OLD':0,'NEW':0}


    ######################################### Fufei resouce BEGIN##################################

    def do_FuFeiAttrOpt(self, json_obj, cache_obj_list):
        update_cache = True
        try:
            site = json_obj['site']
            work_type = json_obj['work_type']
            if 'movie' in work_type:
                #do fufei movie action
                table_name = 'fufei_movie_data_ori'
                for obj in json_obj['obj_list']:
                    if 'payment' not in obj:
                        AttrDbBll.__logger.warning('DISCARD WORK FAILED: payment not in obj, json=%s' %(obj))
                        continue
                    payment = int(obj['payment'])
                    if payment == 0:
                        continue
                    link = obj['link']
                    #check link 
                    normalized_link = Funclib.normalize_url(link)
                    if len(normalized_link) < 5:
                        AttrDbBll.__logger.warning('DISCARD WORK FAILED: normalized_link is empty, json=%s' %(obj))
                        continue
                    #check in db
                    ret = 0
                    #select_sql = "select id, commit_flag from %s where list_link='%s'" %(table_name, link)
                    select_sql = "select id, commit_flag from %s where normalized_link='%s'" %(table_name, normalized_link)
                    ret_data_rows = self.__db_conn.do_QUERY(select_sql)
                    if ret_data_rows is not None and len(ret_data_rows) > 0:
                            AttrDbBll.__logger.info("%d records exist already in data_ori db, sql_cmd=%s" % (len(ret_data_rows), select_sql))
                            #update data status
                            commit_flag = int(ret_data_rows[0][1])
                            if commit_flag != 0:
                                id = int(ret_data_rows[0][0])
                                crawle_flag = '2'
                                crawle_time = str(int(time.time()))
                                update_sql = "update %s set crawle_flag='%s', crawle_time='%s' where id=%d" \
                                        %(table_name, crawle_flag, crawle_time, id)
                                ret = self.__db_conn.do_UPDATE(update_sql)
                                if ret != 0:
                                    AttrDbBll.__logger.warning("update %s db set crawle_flag=2 failed, sql_cmd=%s" % (table_name, sql_gbk))
                            #else: can update crawle data
                            #update cache
                            cache_obj_list.append(obj)
                    else:
                        #insert new obj
                        title = obj['single_title']
                        poster1 = obj['horiz_img']
                        duration = str(obj['duration'])
                        monthly_payment = str(obj['payment'])
                        crawle_flag = '1'
                        crawle_time = str(int(time.time()))
                        #unform title value
                        if type(title) is types.UnicodeType:
                            title = title.encode('utf-8', "ignore")
                        title = MySQLdb.escape_string(title)
                        #discard work_title
                        if len(title) <= 0:
                            AttrDbBll.__logger.warning('DISCARD WORK FAILED: work title is empty, json=%s' %(obj))
                            continue
                        #insert data
                        insert_sql = "insert ignore into %s(site, title, list_link, poster1, duration, Monthlypayment, crawle_flag, crawle_time, normalized_link) \
                                values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                                %(table_name, site, title, link, poster1, duration, monthly_payment, crawle_flag, crawle_time, normalized_link)
                        sql_gbk = insert_sql.decode('utf-8').encode('gbk', 'ignore')
                        ret = self.__db_conn.do_INSERT(sql_gbk)
                        if ret != 0:
                            AttrDbBll.__logger.warning("insert into %s db failed, sql_cmd=%s" % (table_name, sql_gbk))
                        else:
                            cache_obj_list.append(obj)
        except :
            t, v, tb = sys.exc_info()
            AttrDbBll.__logger.warning('error happend in do_FuFeiAttrOpt, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
        return update_cache

    ######################################### Fufei resouce END####################################


    #main operation
    def updateAttrData(self, json_obj, cache_obj_list):
        new_work = True
        work_id = -1

        if cache_obj_list is not None:
            del cache_obj_list[:]
            
        update_cache = False
        data_opt_ret = True
        try:
            #discard fufei or not
            if 'payment' in json_obj:
                payment = int(json_obj['payment'])
                if payment != 0:
                    return self.do_FuFeiAttrOpt(json_obj, cache_obj_list)

            #uniform list_link
            list_link = json_obj['list_link']
            normalized_list_link = Funclib.normalize_url(list_link)
            json_obj['list_link'] = normalized_list_link

            #update db
            site = json_obj['site']
            work_type = json_obj['work_type']

            list_link = json_obj['list_link']
            ret, data_select_sql = self.__genDataSelectSql(work_type, list_link)
            if ret:
                #execute select sql in data_ori
                ret_data_rows = self.__db_conn.do_QUERY(data_select_sql)
                if ret_data_rows is not None:
                    if len(ret_data_rows) > 0:
                        AttrDbBll.__logger.info("%d records exist already in data_ori db, sql_cmd=%s" % (len(ret_data_rows), data_select_sql))
                        new_work = False

                        db_link_list = ret_data_rows[0][0]
                        work_id = ret_data_rows[0][3]

                        get_right_row = False
                        work_id_ok_row = None
                        try:
                            for row in ret_data_rows:
                                work_state = int(row[4])
                                work_is_del = int(row[5])
                                work_tmp_id = int(row[3])
                                if work_tmp_id > 0:
                                    work_id_ok_row = row
                                if work_state==1 and work_is_del==0: 
                                    db_link_list = row[0]
                                    work_id = row[3]
                                    get_right_row = True
                                    break

                            if not get_right_row and work_id_ok_row is not None:
                                db_link_list = work_id_ok_row[0]
                                work_id = work_id_ok_row[3]
                        except :
                            t, v, tb = sys.exc_info()
                            AttrDbBll.__logger.warning('LOOP DATA_ROWS FOR LIST_LINK FAILED, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))


                        json_obj['list_link'] = db_link_list

                    else:
                        AttrDbBll.__logger.info("records not in data_ori db, sql_cmd=%s" % (data_select_sql))
                        new_work = True

                        #discard work_title
                        work_title = json_obj['title'].strip()
                        if len(work_title) <= 0:
                            AttrDbBll.__logger.warning('DISCARD WORK FAILED: work title is empty, json=%s' %(json_obj))
                            #not need, just output log
                            return False

                        # insert into data_ori
                        ret, data_insert_sql = self.__genDataInsertSql(json_obj)
                        if ret:
                            print 'SELECT FROM DATA_ORI: ', data_select_sql
                            print 'INSERT TO DATA_ORI: ', data_insert_sql 
                            ret = 0
                            ret = self.__db_conn.do_INSERT(data_insert_sql)
                            if ret != 0:
                                data_opt_ret = False
                                AttrDbBll.__logger.warning("insert into data_ori db failed, sql_cmd=%s" % (data_insert_sql))

                else:
                    data_opt_ret = False
                    AttrDbBll.__logger.warning("select data_ori db failed, sql_cmd=%s" % (data_select_sql))
            
                if 'movie' in work_type:
                    obj = json_obj['obj_list'][0]
                    if not new_work: 
                        AttrDbBll.__logger.error("OLD_WORK_OLD_OBJ: \t%s\t%s\t%d\t%s\t%s\t%s\t%s" % (site, work_type, work_id, obj['single_title'], list_link, str(obj['episode']), obj['link']))
                    else:
                        AttrDbBll.__logger.error("NEW_WORK_NEW_OBJ: \t%s\t%s\t%s\t%s\t%s\t%s" % (site, work_type, obj['single_title'], list_link, str(obj['episode']), obj['link']))

                if "movie" not in work_type:
                    for obj in json_obj['obj_list']:
                        ret, reason = self.__discardInfo(work_type, obj)
                        if not ret:
                            AttrDbBll.__logger.warning('discard infomation failed, json=%s' %(obj))
                            continue

                        episode = obj['episode']
                        link = obj['link']
                        list_link = json_obj['list_link']

                        if new_work: 
                            AttrDbBll.__logger.error("NEW_WORK_NEW_OBJ: \t%s\t%s\t%s\t%s\t%s\t%s" % (site, work_type, json_obj['title'], list_link, str(episode), link))

                        ret, obj_select_sql = self.__genObjSelectSql(work_type, list_link, episode)
                        if ret:
                            obj_flag_dead = False
                            #execute select sql in obj_ori
                            ret_obj_rows = self.__db_conn.do_QUERY(obj_select_sql)
                            if ret_obj_rows is not None:
                                if len(ret_obj_rows) > 0:
                                    obj_flag_dead = True
                                    try:
                                        for row in ret_obj_rows:
                                            dead_flag = int(row[0])
                                            if dead_flag != 1: 
                                                obj_flag_dead = False
                                                break
                                    except :
                                        obj_flag_dead = False
                                        t, v, tb = sys.exc_info()
                                        AttrDbBll.__logger.warning('LOOP OBJ_ROWS FOR OBJ_FLAG_DEAD FAILED, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
                                        
                                    if not obj_flag_dead:
                                        AttrDbBll.__logger.info("%d records exist already in obj_ori db, sql_cmd=%s" % (len(ret_obj_rows), obj_select_sql))
                                        if not new_work:
                                            AttrDbBll.__logger.error("OLD_WORK_OLD_OBJ: \t%s\t%s\t%d\t%s\t%s\t%s\t%s" % (site, work_type, work_id, json_obj['title'], list_link, str(episode), link))
                                        if data_opt_ret:
                                            #update cache
                                            update_cache = True
                                            cache_obj_list.append(obj)

                                if len(ret_obj_rows) <= 0 or obj_flag_dead:
                                    AttrDbBll.__logger.info("records not in obj_ori db or dead in obj_ori, rows_len=%d, dead_flag=%s, sql_cmd=%s" % (len(ret_obj_rows), str(obj_flag_dead),obj_select_sql))
                                    # insert into obj_ori
                                    ret, obj_insert_sql = self.__genObjInsertSql(work_type, list_link, site, obj)
                                    if ret:
                                        print 'SELECT FROM OBJ_ORI: ', obj_select_sql
                                        print 'INSERT TO OBJ_ORI: ', obj_insert_sql
                                        ret = 0
                                        ret = self.__db_conn.do_INSERT(obj_insert_sql)
                                        if ret != 0:
                                            AttrDbBll.__logger.warning("insert into obj_ori db failed, sql_cmd=%s" % (obj_insert_sql))
                                        else:
                                            if not new_work:
                                                AttrDbBll.__logger.error("OLD_WORK_NEW_OBJ: \t%s\t%s\t%d\t%s\t%s\t%s\t%s" % (site, work_type, work_id, json_obj['title'], list_link, str(episode), link))

                                            if data_opt_ret:
                                                #update cache
                                                update_cache = True
                                                cache_obj_list.append(obj)
                            else:
                                AttrDbBll.__logger.warning("select obj_ori db failed, sql_cmd=%s" % (obj_select_sql))
                elif data_opt_ret:
                    #update cache
                    update_cache = True
                    obj = json_obj['obj_list'][0]
                    cache_obj_list.append(obj)
                    
                    return update_cache
                                
        except :
            update_cache = False
            t, v, tb = sys.exc_info()
            AttrDbBll.__logger.warning('parse json in updateAttrData failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))

        return update_cache


