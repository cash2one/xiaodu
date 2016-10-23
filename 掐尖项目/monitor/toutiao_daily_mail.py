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

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)-5s %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', filename='toutiao_mail.log')


def today_date():
    """brief: """
    return datetime.now().strftime('%Y-%m-%d')


def yesterday_date():
    """brief: """
    ts = datetime.now() - timedelta(days=1)
    return ts.strftime('%Y-%m-%d')
    

user_count_sql = 'select count(*) from user_result where site_id=8'
obj_count_sql = 'select count(*) from obj_result where site_id=8'

incr_user_sql = 'select count(*) from user_result where site_id=8 and \
    create_time >= "{yesterday}" and create_time < "{today}"'.format(
        yesterday=yesterday_date(), today=today_date())
incr_obj_sql = 'select count(*) from obj_result where site_id=8 and \
    create_time >= "{yesterday}" and create_time < "{today}"'.format(
        yesterday=yesterday_date(), today=today_date())


def execute_count_sql(cursor, sql):
    """brief: """
    #logging.debug(sql)
    cursor.execute(sql)
    count, = cursor.fetchone()
    return count

    
def collect_data(cursor):
    """brief: """
    user_count = execute_count_sql(cursor, user_count_sql)
    obj_count = execute_count_sql(cursor, obj_count_sql)
    incr_user_num = execute_count_sql(cursor, incr_user_sql)
    incr_obj_num = execute_count_sql(cursor, incr_obj_sql)
    date = today_date()

    return dict(user_count=user_count, obj_count=obj_count, 
        incr_user_num=incr_user_num, incr_obj_num=incr_obj_num, date=date)


def send_mail(data):
    """brief: """
    import toutiao_mail_conf as conf
    subject = conf.subject.format(**data).decode('utf-8').encode('gb18030')
    content = conf.content.format(**data).decode('utf-8').encode('gb18030')

    echo_commands = ['echo', content]
    logging.debug(echo_commands)
    
    mail_commands = ['mail', '-s', subject]
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
        conn = MySQLdb.connect(user='root', db='ec_task')
        data = collect_data(conn.cursor())
        send_mail(data)
    except:
        logging.exception('something wrong')


if __name__ == '__main__':
    main()
