#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/11/29 下午2:49
# @Author  : Sheng Zeng
# @Site    :
# @File    : conf.py
# @Software: PyCharm
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
redis_conf = {
    'host': '10.143.149.46',
    'port': 6379,
    'db': 1,
}
