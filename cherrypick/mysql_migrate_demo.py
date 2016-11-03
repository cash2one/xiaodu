#ecoding:utf-8
import sys
import json
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")

import six
from six import iteritems
from six import itervalues
import mysql.connector
import os,re
class BaseDB:

    '''
    BaseDB
    dbcur should be overwirte
    '''
    __tablename__ = None
    placeholder = '%s'

    @staticmethod
    def escape(string):
        return '`%s`' % string

    @property
    def dbcur(self):
        raise NotImplementedError

    def _execute(self, sql_query, values=[]):
        dbcur = self.dbcur
        dbcur.execute(sql_query, values)
        return dbcur

    def _select(self, tablename=None, what="*", where="", where_values=[], offset=0, limit=None):
        tablename = self.escape(tablename or self.__tablename__)
        if isinstance(what, list) or isinstance(what, tuple) or what is None:
            what = ','.join(self.escape(f) for f in what) if what else '*'

        sql_query = "SELECT %s FROM %s" % (what, tablename)
        if where:
            sql_query += " WHERE %s" % where
        if limit:
            sql_query += " LIMIT %d, %d" % (offset, limit)
        #logger.debug("<sql: %s>", sql_query)

        for row in self._execute(sql_query, where_values):
            yield row

    def _select2dic(self, tablename=None, what="*", where="", where_values=[],
                    order=None, offset=0, limit=None):
        tablename = self.escape(tablename or self.__tablename__)
        if isinstance(what, list) or isinstance(what, tuple) or what is None:
            what = ','.join(self.escape(f) for f in what) if what else '*'

        sql_query = "SELECT %s FROM %s" % (what, tablename)
        if where:
            sql_query += " WHERE %s" % where
        if order:
            sql_query += ' ORDER BY %s' % order
        if limit:
            sql_query += " LIMIT %d, %d" % (offset, limit)
        #print ("<sql: %s>", sql_query)

        dbcur = self._execute(sql_query, where_values)
        fields = [f[0] for f in dbcur.description]
        #print sql_query

        for row in dbcur:
            yield dict(zip(fields, row))

    def _replace(self, tablename=None, **values):
        tablename = self.escape(tablename or self.__tablename__)
        if values:
            _keys = ", ".join(self.escape(k) for k in values)
            _values = ", ".join([self.placeholder, ] * len(values))
            sql_query = "REPLACE INTO %s (%s) VALUES (%s)" % (tablename, _keys, _values)
        else:
            sql_query = "REPLACE INTO %s DEFAULT VALUES" % tablename
        #logger.debug("<sql: %s>", sql_query)

        if values:
            dbcur = self._execute(sql_query, list(itervalues(values)))
        else:
            dbcur = self._execute(sql_query)
        return dbcur.lastrowid

    def _insert(self, tablename=None, **values):
        tablename = self.escape(tablename or self.__tablename__)
        if values:
            _keys = ", ".join((self.escape(k) for k in values))
            _values = ", ".join([self.placeholder, ] * len(values))
            sql_query = "INSERT INTO %s (%s) VALUES (%s)" % (tablename, _keys, _values)
        else:
            sql_query = "INSERT INTO %s DEFAULT VALUES" % tablename
        #logger.debug("<sql: %s>", sql_query)

        if values:
            dbcur = self._execute(sql_query, list(itervalues(values)))
        else:
            dbcur = self._execute(sql_query)
        return dbcur.lastrowid

    def _update(self, tablename=None, where="1=0", where_values=[], **values):
        tablename = self.escape(tablename or self.__tablename__)
        _key_values = ", ".join([
            "%s = %s" % (self.escape(k), self.placeholder) for k in values
        ])
        sql_query = "UPDATE %s SET %s WHERE %s" % (tablename, _key_values, where)
        #print ("<sql: %s>", sql_query)

        return self._execute(sql_query, list(itervalues(values)) + list(where_values))

    def _delete(self, tablename=None, where="1=0", where_values=[]):
        tablename = self.escape(tablename or self.__tablename__)
        sql_query = "DELETE FROM %s" % tablename
        if where:
            sql_query += " WHERE %s" % where
        #logger.debug("<sql: %s>", sql_query)

        return self._execute(sql_query, where_values)


class DB(BaseDB):
    __tablename__ = "crawl_data_demo"

    def __init__(self):
        config = {'host': '180.76.157.65',  # 默认127.0.0.1
                  'user': 'app',
                  'password': 'app',
                  'port': 3336,  # 默认即为3306
                  'database': 'app_db',
                  'charset': 'utf8' ,
                  'autocommit' : True
                  }

        self.conn = mysql.connector.connect(**config)
        self.database_name = 'app_db'

    @property
    def dbcur(self):
        try:
            if self.conn.unread_result:
                self.conn.get_rows()
            return self.conn.cursor()
        except (mysql.connector.OperationalError, mysql.connector.InterfaceError):
            self.conn.ping(reconnect=True)
            self.conn.database = self.database_name
            return self.conn.cursor()

class DB2(BaseDB):
    __tablename__ = "crawl_data"

    def __init__(self):
        config = {'host': '10.114.32.36',  # 默认127.0.0.1
                  'user': 'video',
                  'password': 'video',
                  'port': 9306,  # 默认即为3306
                  'database': 'cherrypick_db',
                  'charset': 'utf8' ,
                  'autocommit' : True
                  }

        self.conn = mysql.connector.connect(**config)
        self.database_name = 'cherrypick_db'

    @property
    def dbcur(self):
        try:
            if self.conn.unread_result:
                self.conn.get_rows()
            return self.conn.cursor()
        except (mysql.connector.OperationalError, mysql.connector.InterfaceError):
            self.conn.ping(reconnect=True)
            self.conn.database = self.database_name
            return self.conn.cursor()

db = DB2()
insert_db = DB()

from pyspider.libs.check import CheckData
check_data=CheckData()
import urllib
import urllib2
import hashlib
import sys
import socket  
timeout = 10    
socket.setdefaulttimeout(timeout)

def get_timgurl(imgurl, isForce=0, size=10, intQuality=100, intCutX=None, intCutY=None, intCutW=None, intCutH=None):
    if imgurl == None:
        return None
    # 使用图云压图供第三方使用
    key  = 'wisetimgkey_noexpire_3f60e7362b8c23871c7564327a31d9d7'
    sec  = '1366351082'
    dicParam = {}
    if intCutX != None:
        dicParam['cut_x'] = intCutX
    if intCutY != None:
        dicParam['cut_y'] = intCutY
    if intCutW != None:
        dicParam['cut_w'] = intCutW
    if intCutH != None:
        dicParam['cut_h'] = intCutH
    dicParam['quality'] = intQuality
    dicParam['size']    = size
    dicParam['sec']     = sec
    m1 = hashlib.md5()
    m1.update(key + sec + imgurl)
    dicParam['di'] = m1.hexdigest()
    # 原图url(仅保证http协议)。支持URLEncode格式和URLDecode格式（使用cdn时，必须是URLEncode）。注意计算di时需要使用未URLDecode的格式。并且注意src必须为整个请求的最后一个参数
    dicParamsrc = {}
    dicParamsrc['src'] = imgurl
    new_imgurl  = 'http://timg.baidu.com/timg?video&' + urllib.urlencode(dicParam) + '&' + urllib.urlencode(dicParamsrc)
    try:
        response = urllib2.urlopen(new_imgurl)
        response_text = response.read()
        #print response_text
    except Exception as ex:
        print ex
        return None

    return new_imgurl

def process():
    try:
        for result in list(db._select2dic(offset=240000,limit=50000)):
                result['app_name'] = result['site']
                result['thumnail_url'] = result['horizontal_thumnail_url']
                if result['thumnail_url'] == '':
                    result['thumnail_url'] = result['vertical_thumnail_url']
                try:
                    t_img = get_timgurl(result['thumnail_url'])
                except Exception as ee:
                    print ee
                    continue
                if t_img:
                    result['thumnail_url'] = t_img
                else:
                    continue
                result.pop('horizontal_thumnail_url')
                result.pop('vertical_thumnail_url')
                result.pop('down_count')
                result.pop('site')
                result.pop('definition_qlevel')
                result.pop('flag_dead')
                result.pop('page_id')
                result.pop('horizontal_thumnail_sign1')
                result.pop('horizontal_thumnail_sign2')
                result.pop('vertical_thumnail_sign1')
                result.pop('vertical_thumnail_sign2')
                result.pop('link_sign1')
                result.pop('link_sign2')
                result.pop('horizontal_thumnail_score')
                result.pop('vertical_thumnail_qlevel')
                result.pop('title_qlevel')
                result.pop('duration')
                result.pop('hd')
                result.pop('real_link')
                try:
                    insert_db._insert(tablename='crawl_data_demo',**result)          
                    print '数据插入成功'
                    #break
                except Exception as ee:
                    print ee
                    continue
    except:
        traceback.print_exc()

if __name__ == '__main__':
    process()
