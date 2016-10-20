# -*- coding: utf-8 -*-
__author__ = 'yangxiaoyun'
#统计content中某个属性的字段值

import sys
#import MySQLdb
import json
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")

import six
from six import iteritems
from six import itervalues
import mysql.connector
import os
import logging
import logging.config
logging.config.fileConfig("./conf/logging.conf")
#create logger
logger = logging.getLogger('data_compute')
#"application" code

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
        #logger.debug("<sql: %s>", sql_query)

        dbcur = self._execute(sql_query, where_values)
        fields = [f[0] for f in dbcur.description]

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
    __tablename__ = ""
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




class DataOperation():
    def __init__(self):
        self.db=DB()



    def picFill(self, table, output_file_path):
        try:
            file = open(output_file_path, 'w')
            #sql = 'select taskid,result from %s' %(table)
            what = ['taskid','result']
            for each in self.db._select2dic(tablename=table, what=what):
                #print each['taskid'],each['result']
                file.write('%s$$$$$%s\n' %(str(each['taskid']), json.dumps(str(each['result']))))
                file.flush()
                #break
            file.close()
        except Exception as ee:
            print ee.message
            logger.error('downloadData faild')

    def idGenerate(self, table, output_file_path):
        try:
            file = open(output_file_path, 'w')
            # sql = 'select taskid,result from %s' %(table)
            what = ['taskid', 'result']
            for each in self.db._select2dic(tablename=table, what=what):
                # print each['taskid'],each['result']
                file.write('%s$$$$$%s\n' % (str(each['taskid']), json.dumps(str(each['result']))))
                file.flush()
                # break
            file.close()
        except Exception as ee:
            print ee.message
            logger.error('downloadData faild')

    def dataParse(self, origin_data):
        try:
            arr = origin_data.split('$$$$$')
            #print arr
            taskid = arr[0]
            #data_json = arr[1].replace('\\\\','\\')
            #print data_json
            #print 'json__',json.loads(arr[1])
            #for k, v in data.iteritems():
             #   print k , v
            #return json.dumps(data)
            return json.loads(json.loads(arr[1]))
        except Exception as ee:
            print ee.message
            logger.error('dataParse faild: %s---%s' % (ee.message,taskid))



if __name__=="__main__":
 #   pdb.set_trace()
    db = DB()
    result_file_name = sys.argv[1]
    DP = DataOperation()
    for line in sys.stdin:
        #print line
        result = DP.dataParse(line.strip())
        if not result:
            logger.debug('数据质量差：%s' % result)
            continue
        #fw.write(result+'\n')
        #fw.flush()
        try:
            if type(result) == dict:
                result['app_name'] = result['site']
                result['thumnail_url'] = result['horizontal_thumnail_url']
                if result['thumnail_url'] == '':
                    result['thumnail_url'] = result['vertical_thumnail_url']
                result.pop('horizontal_thumnail_url')
                result.pop('vertical_thumnail_url')
                result.pop('down_count')
                result.pop('site')
                db._insert(tablename='crawl_data_test',**result)
                print '数据插入成功'
                logger.info('数据插入成功: %s' % result_file_name)
            if type(result) == list:
                for each in result:
                    db._insert(tablename='crawl_data_test', **each)
                    print '数据插入成功'
                    logger.info('数据插入成功: %s' % result_file_name)
        except Exception as ee:
            #print result
            print ee
            logger.error('数据插入失败: %s' % ee)
    print '数据处理完毕'




