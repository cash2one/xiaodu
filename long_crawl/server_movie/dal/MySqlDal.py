#!/bin/env python
#-*- encoding:utf-8 -*-

import MySQLdb
import sys
import traceback
from utils.LogUtil import Logger

class pyMySQL():
    __logger = Logger.get_logger()

    def __init__(self, host, user, passwd, dbname, port = '3306', char_set ='gbk'):
        self.bConned = False
        self.dbHandle = None
        self.host = host
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.port = int(port)
        self.char_set = char_set
        


    def __del__(self):
        self.disconnect_to_mysql()
        pyMySQL.__logger.debug('disconnect_to_mysql() success, host=%s, user=%s, db=%s, port=%u' % (self.host, self.user, self.dbname, self.port))
        

    def connect_to_mysql(self, char_set = None):
        try:
            if True == self.bConned:
                return True
            if char_set is None:
                db_char_set = self.char_set
            else:
                db_char_set = char_set
            self.dbHandle = MySQLdb.connect(host = self.host, user = self.user, passwd = self.passwd, db = self.dbname, port = self.port, charset = db_char_set, connect_timeout=30)
            self.bConned = True
            pyMySQL.__logger.debug('Connect to MySQL Server success, host=%s, user=%s, db=%s, port=%u' % (self.host, self.user, self.dbname, self.port))
            return True 
        except Exception, e:
            self.disconnect_to_mysql()
            pyMySQL.__logger.warning('Connect to MySQL Server Failed, host=%s, user=%s, db=%s, port=%u, errmsg=%s' % (self.host, self.user, self.dbname, self.port, e))
            return False


    def disconnect_to_mysql(self):
        try:    
            if (True == self.bConned) and (self.dbHandle is not None):
                self.dbHandle = None
                self.bConned = False
                #self.dbHandle.close()
        except Exception, e:
            pyMySQL.__logger.warning('Disconnect to MySQL Server Failed, errmsg=%s' % (e))
            

    def do_QUERY(self, sql_cmd):
        try:
            retry = 0
            if (False == self.bConned) or (self.dbHandle is None):
                if True != self.connect_to_mysql():
                    pyMySQL.__logger.warning('do_QUERY() failed: self.dbHandle = None')
                    return None
            while True:
                try:
                    # if connected, do the query
                    cursor = self.dbHandle.cursor()
                    cursor.execute(sql_cmd)
                    rows = cursor.fetchall()
                    self.dbHandle.commit() 
                    cursor.close()
                    pyMySQL.__logger.debug('query completed, %d records fetched from mysql server' % (len(rows)))
                    return rows
                except:
                    #self.dbHandle.rollback()
                    retry = retry + 1
                    if retry > 3:
                        raise Exception('do_QUERY failed and retry > 3!')
                    else:
                        self.disconnect_to_mysql()
                        if not self.connect_to_mysql():
                            pyMySQL.__logger.warning('do_QUERY() failed: self.dbHandle = None')
                            return None
        except Exception, e:
            t, v, tb = sys.exc_info()
            self.disconnect_to_mysql()
            pyMySQL.__logger.warning('do_QUERY() failed, errmsg=%s ,%s,%s,%s' % (e, t, v, traceback.format_tb(tb)))
            return None


    def do_INSERT(self, sql_cmd):
        try:
            if (False == self.bConned) or (self.dbHandle is None):
                if True != self.connect_to_mysql():
                    pyMySQL.__logger.warning('do_QUERY() failed: self.dbHandle = None')
                    return None
            # if connected, do the insert operation
            cursor = self.dbHandle.cursor()
            cursor.execute(sql_cmd)
            self.dbHandle.commit() 
            cursor.close()
            pyMySQL.__logger.debug('insert completed, return success')
            return 0
        except Exception, e:
            pyMySQL.__logger.warning('do_INSERT() failed, errmsg=%s' % (e))
            try:
                self.dbHandle.rollback()
            except Exception, ex:
                pyMySQL.__logger.warning('self.dbHandle.rollback in do_INSERT() failed, errmsg=%s' % (ex))
            self.disconnect_to_mysql()
            return None


    def do_UPDATE(self, sql_cmd):
        try:
            if (False == self.bConned) or (self.dbHandle is None):
                if True != self.connect_to_mysql():
                    pyMySQL.__logger.warning('do_QUERY() failed: self.dbHandle = None')
                    return None
            # if connected, do the update operation
            cursor = self.dbHandle.cursor()
            cursor.execute(sql_cmd)
            self.dbHandle.commit() 
            cursor.close()
            pyMySQL.__logger.debug('update completed, return success')
            return 0
        except Exception, e:
            pyMySQL.__logger.warning('do_UPDATE() failed, errmsg=%s' % (e))
            try:
                self.dbHandle.rollback()
            except Exception, ex:
                pyMySQL.__logger.warning('self.dbHandle.rollback in do_UPDATE() failed, errmsg=%s' % (ex))
            self.disconnect_to_mysql()
            return None

    def do_DELETE(self, sql_cmd):
        try:
            if (False == self.bConned) or (self.dbHandle is None):
                if True != self.connect_to_mysql():
                    pyMySQL.__logger.warning('do_QUERY() failed: self.dbHandle = None')
                    return None
            # if connected, do the delete operation
            cursor = self.dbHandle.cursor()
            cursor.execute(sql_cmd)
            self.dbHandle.commit() 
            cursor.close()
            pyMySQL.__logger.debug('delete completed, return success')
            return 0
        except Exception, e:
            pyMySQL.__logger.warning('do_DELETE() failed, errmsg=%s' % (e))
            try:
                self.dbHandle.rollback()
            except Exception, ex:
                pyMySQL.__logger.warning('self.dbHandle.rollback in do_DELETE() failed, errmsg=%s' % (ex))
            self.disconnect_to_mysql()
            return None
