#-*-coding:gbk-*-
'''
Created on 2014-7-29
@author: wsx
'''

import os
import sys
import traceback

#set encode
reload(sys)
sys.setdefaultencoding("gbk")

f_path = os.path.dirname(__file__)                                                                                                                                                       
if len(f_path) < 1: f_path = "."
sys.path.append(f_path)
sys.path.append(f_path + "/..")

from dal.MySqlDal import pyMySQL
from conf.DBConfig import DBConfig


class GenSQLFromDB(object):
    db_config = DBConfig()
    
    def __init__(self):
        self.__db_handle = None
        
    def init_db_handle(self):
        ret = True
        try:
            if self.__db_handle is None:
                self.__db_handle = pyMySQL(GenSQLFromDB.db_config.MYSQL['host'],
                                           GenSQLFromDB.db_config.MYSQL['uname'], 
                                           GenSQLFromDB.db_config.MYSQL['pwd'], 
                                           GenSQLFromDB.db_config.MYSQL['db_name'], 
                                           GenSQLFromDB.db_config.MYSQL['port'], 
                                           GenSQLFromDB.db_config.MYSQL['encoding'])
        except Exception as e:
            t, v, tb = sys.exc_info()
            print('init_db_handle failed, errmsg=%s,%s,%s' % (t, v, traceback.format_tb(tb)))
            ret = False
            self.__db_handle = None
        return ret
    
    def normalize_url(self, url):
        index = url.find('?')
        if index != -1:
            new_url = url[:index].strip()
            return new_url
        return url.strip()

        
    def gen_init_normalizedLinkField_sql(self, file_path):
        if not file_path.endswith("/"):
            file_path = file_path + "/"
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_name = file_path + "movie_data_ori_normalized_list_link.txt"
        with open(file_name, "a+") as url_file:
            select_sql = "select link, link_sign1, link_sign2 from movie_data_ori"
            update_sql = "update movie_data_ori set normalized_link='%s' where link_sign1=%d and link_sign2=%d;\n"
            rows = self.__db_handle.do_QUERY(select_sql)
            for row in rows:
                link = row[0]
                new_link = self.normalize_url(link)
                url_file.write(new_link+"\n")
    
    def gen_init_normalizedListLinkField_sql(self, file_path):
        if not file_path.endswith("/"):
            file_path = file_path + "/"
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        #comic
        file_name = file_path + "comic_data_ori_normalized_list_link.txt"
        with open(file_name, "a+") as url_file:
            select_sql = "select list_link, sign1, sign2 from comic_data_ori"
            update_sql = "update comic_data_ori set normalized_list_link='%s' where sign1=%d and sign2=%d;\n"
            rows = self.__db_handle.do_QUERY(select_sql)
            for row in rows:
                list_link = row[0]
                new_list_link = self.normalize_url(list_link)
                url_file.write(new_list_link+"\n")
                
        #show
        file_name = file_path + "shows_data_ori_normalized_list_link.txt"
        with open(file_name, "a+") as url_file:
            select_sql = "select list_link, sign1, sign2 from shows_data_ori"
            update_sql = "update shows_data_ori set normalized_list_link='%s' where sign1=%d and sign2=%d;\n"
            rows = self.__db_handle.do_QUERY(select_sql)
            for row in rows:
                list_link = row[0]
                new_list_link = self.normalize_url(list_link)
                url_file.write(new_list_link+"\n")
                
        #tvplay
        file_name = file_path + "tvplay_data_ori_normalized_list_link.txt"
        with open(file_name, "a+") as url_file:
            select_sql = "select list_link, sign1, sign2 from tvplay_data_ori"
            update_sql = "update tvplay_data_ori set normalized_list_link='%s' where sign1=%d and sign2=%d;\n"
            rows = self.__db_handle.do_QUERY(select_sql)
            for row in rows:
                list_link = row[0]
                list_link_sign1 = row[1]
                list_link_sign2 = row[2]
                new_list_link = self.normalize_url(list_link)
                url_file.write(new_list_link+"\n")


if __name__ == '__main__':
    gensql = GenSQLFromDB()
    if gensql.init_db_handle():
        #for movie
        gensql.gen_init_normalizedLinkField_sql("./links")
        #for tv,comic,show
        gensql.gen_init_normalizedListLinkField_sql("./links")
        print 'DONE!!!'
