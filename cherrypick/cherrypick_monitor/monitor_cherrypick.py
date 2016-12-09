#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Author: Shangshuaipen Li Dongye
# Date: 2016-10-17 20:10:38

"""
Brief: 
"""

import MySQLdb
from datetime import datetime
from datetime import timedelta
import subprocess
import logging
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)-5s %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', filename='cherrypick_db.log')


def yesterday_date():
    """brief: """
    ts = int(time.mktime(time.strptime(time.strftime('%Y-%m-%d',time.localtime()),'%Y-%m-%d'))) - 86400
    return ts

def today_date():
    """brief: """
    return int(time.mktime(time.strptime(time.strftime('%Y-%m-%d', time.localtime()), '%Y-%m-%d')))
    

site_count_sql = 'SELECT site,count(*) as sum FROM crawl_data group by site'
block_count_sql = 'SELECT block,count(*) as sum FROM crawl_data where site!="wangyiclass" group by block'
class_count_sql = 'SELECT block,count(*) as sum FROM crawl_data where site="wangyiclass" group by block'

inc_site_sql = 'select site,count(*) from crawl_data where insert_time >= {yesterday} and insert_time < {today} group by site'.format(
    yesterday=yesterday_date(), today=today_date())

inc_block_sql = 'select block,count(*) from crawl_data where insert_time >= {yesterday} and insert_time < {today} and site!="wangyiclass" group by block'.format(
    yesterday=yesterday_date(), today=today_date())

inc_class_sql = 'select block,count(*) from crawl_data where insert_time >= {yesterday} and insert_time < {today} and site="wangyiclass" group by block'.format(
    yesterday=yesterday_date(), today=today_date())

site_source_sql = 'select distinct block,site from crawl_data where site!="wangyiclass" group by block,site'

def execute_count_sql(cursor, sql):
    """brief: """
    #logging.debug(sql)
    cursor.execute(sql)
    _list = []
    for (temp,count) in cursor.fetchall():
        _dict = {}
        _dict[temp] = count
        _list.append(_dict)
    return _list

monitor_dict = {
    'site_count':'2、各站点已抓取视频总量(公开课除外):\n',
    'block_count':'4、各频道已抓取视频总量(公开课除外):\n',
    'class_count':'6、网易公开课已抓取视频总量:\n',
    'inc_site_num':'1、各站点昨日新增视频(公开课除外):\n',
    'inc_block_num':'3、各频道昨日新增视频(公开课除外):\n',
    'inc_class_num':'7、网易公开课各频道昨日新增视频:\n',
    'site_source':'5、各频道抓取的来源站点:\n',
}
monitor_list = [
    'inc_site_num',
    'site_count',
    'inc_block_num',
    'block_count',
    'site_source',
    'class_count',
    'inc_class_num',
]
    
def collect_data(cursor):
    """brief: """
    site_count = execute_count_sql(cursor, site_count_sql)
    block_count = execute_count_sql(cursor, block_count_sql)
    class_count = execute_count_sql(cursor, class_count_sql)
    inc_site_num = execute_count_sql(cursor, inc_site_sql)
    inc_block_num = execute_count_sql(cursor, inc_block_sql)
    inc_class_num = execute_count_sql(cursor, inc_class_sql)
    site_source = execute_count_sql(cursor, site_source_sql)
    date = time.strftime('%Y-%m-%d', time.localtime())

    return dict(site_count=site_count, block_count=block_count, class_count=class_count,
                inc_site_num=inc_site_num, inc_block_num=inc_block_num,inc_class_num=inc_class_num, site_source=site_source, date=date)

def send_mail(data):
    """brief: """
    import cherry_pick_mail_conf as conf
    #subject = conf.subject.format(**data).decode('utf-8').encode('gb18030')
    #content = conf.content.format(**data).decode('utf-8').encode('gb18030')
    subject = "cherrypick抓取情况 %s" % data['date']
    fw = open('/home/video/monitor/log/%s' % data['date']+'.log','a')
    subject = subject.decode('utf8').encode('gb2312')#+'\nContent-Type: text/html;charset=utf8'
    content = ""
    for each1 in monitor_list:
        content += monitor_dict[each1]
        if each1 == 'site_source':
            content += '<table border="1">'
            temp_dict = {}
            for each in data[each1]:
                for k1, v1 in each.iteritems():
                    if temp_dict.has_key(k1):
                        temp_dict[k1] += v1+','
                    else:
                        temp_dict[k1] = v1+','
            for k1,v1 in temp_dict.iteritems():
                content += '<tr><td>' + k1 + '</td><td>' + v1 + '</td></tr>'
            content += '</table>\n'
            continue
        if len(data[each1]) == 0:
            content += '无\n'
            continue
        content += '<table border="1">'
        sum_count = 0
        for each in data[each1]:
            for k1, v1 in each.iteritems():
                sum_count += v1
        content += '<tr><td>总量</td><td>'+str(sum_count)+'</td></tr>'
        for each in data[each1]:
            for k1,v1 in each.iteritems():
                content += '<tr><td>'+k1.encode('utf8')+'</td><td>'+str(v1)+'</td></tr>'
        content +='</table>\n'
    fw.write(content)
    fw.flush()
    fw.close()
    echo_commands = ['echo',content]
    logging.debug(echo_commands)

    mail_commands = ['mail', '-s', subject,'\nContent-Type: text/html;charset=utf-8']
    for cc in conf.copy_to:
        mail_commands.extend(['-c', cc])
    mail_commands.extend(conf.receivers)
    logging.debug(mail_commands)
    echo = subprocess.Popen(echo_commands, stdout=subprocess.PIPE)
    mail = subprocess.Popen(mail_commands, stdin=echo.stdout)
    mail.communicate()


def main():
    """brief: entry"""
    logging.debug('running...')
    try:
        # default localhost
        conn = MySQLdb.connect(host="10.114.32.36", user="video", passwd="video", db="cherrypick_db", charset="utf8",
                               port=9306)
        data = collect_data(conn.cursor())

        send_mail(data)
    except:
        logging.exception('something wrong')


if __name__ == '__main__':
    main()


