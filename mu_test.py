#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/11/28 下午4:30
# @Author  : Sheng Zeng
# @Site    : 
# @File    : multiprocess_one.py
# @Software: PyCharm
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import threading
import time
def func(msg):
    while 1:
        print msg
        time.sleep(1)
        

if __name__ == '__main__':
    threads = []
    for idx in xrange(5):
        msg = "hello %d" % (idx)
        threads.append(threading.Thread(target=func, args=(msg,)))
    for t in threads:
        t.start()

