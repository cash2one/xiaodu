#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/11/2 下午4:37
# @Author  : Sheng Zeng
# @Site    : 
# @File    : query构造解析.py
# @Software: PyCharm
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2,json,re
import socket
socket.setdefaulttimeout(3)
import logging.config
logging.config.fileConfig("logging.conf")
#create logger
logger = logging.getLogger("get_info_by_query")
i = 0
baidu_fw = open('./other/urls_baidu.com','a')
error_query_fw = open('./other/error.query','a')
try:
    filename = sys.argv[1]
except:
    logger.error(u'参数输入错误,例子——python parse_query.py 文件地址')
logger.info(u'query文件地址:%s' % filename)
for line in open(filename):
    query = line.split()[0]
    url = 'http://v.baidu.com/v?word='+query+'&rn=60&ct=905969664&ie=utf-8&du=0&pd=0&sc=0&pn=%s&order=0&db=0&_=1434102847165'
    logger.info(u'构造的url:%s' % url)
    try:
        data = urllib2.urlopen(url).read()
        data =  json.loads(data[14:-1])
    except Exception as ee:
        logger.error(u'打开或解析出错-%s:%s' % (query,ee))
        error_query_fw.write(query+'\n')
        error_query_fw.flush()
        continue
    #print data
    if data.has_key('data'):
        for each in data['data']:
            target_url = each['origin_url']
            pic = each['pic']
            if 'http://baidu.' in target_url or 'http://baishi.' in target_url:
                baidu_fw.write(target_url+'\n')
                baidu_fw.flush()
                continue
            temp_arr = target_url.split('//')[1].split('/')[0].split('.')
            site = temp_arr[-2]+'.'+temp_arr[-1]
            try:
                fw = open('./data/urls_'+site,'a')
                fw.write(target_url+'\t'+pic+'\n')
                fw.flush()
                fw.close()
            except Exception as ee:
                logger.error(u'./data/urls_%s文件打开出错:%s' % (site,ee))
    else:
        logger.info(u'该query无数据:%s' % (query))
        error_query_fw.write(query + '\n')
        error_query_fw.flush()
