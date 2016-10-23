#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Author: Shangshuaipen Li Dongye
# Date: 2016-10-17 20:10:38

"""
Brief: 
"""
receivers = [
    'shangshuaipen@itv.baidu.com', 
    'chenpengjun@itv.baidu.com',
    'maguangming@itv.baidu.com',
    ]
copy_to = [
    'yulei@itv.baidu.com', 
    'liyemin@itv.baidu.com', 
    'hanwei@itv.baidu.com', 
    'huhao@itv.baidu.com', 
    'wujian@itv.baidu.com', 
    'qiuhao@itv.baidu.com',
    ]
#receivers = ['shangshuaipen@itv.baidu.com']
#copy_to = []

subject = "PGC抓取情况 {date}"
content = """
昨日新增用户：{incr_user_num}
昨日新增obj：{incr_obj_num}

已抓取用户总量：{user_count}
已抓取obj总量：{obj_count}
"""
