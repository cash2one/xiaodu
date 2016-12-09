#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-10-17 13:51:29
# Authors: Dongye Li
"""
Brief: 
    send package to mimod
    the package format is nshead+mcpack
"""

import sys
import socket
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("./pyspider/pyspider-0.3.8/pyspider/libs/mcpack")
from pyspider.libs import nshead
import mcpack

def send_to_mimod(item, req_type=1):
    """
    Brief:  send_to_mimod
    Params:
        [dict] item 
        [int] req_type=1 must
    """
    #ret infomation
    ret = 0
    resp_code = 0
    resp_content = "xxx"
    #video_class server
    ip = "10.114.32.36"
    port = 8444
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #1.build request pack
        ##@content
        body = {
            'request_type': mcpack.INT32(req_type),
            'title': mcpack.STR(item['title']),
            'horizontal_thumnail_url': mcpack.STR(item['horizontal_thumnail_url']),
            'vertical_thumnail_url': mcpack.STR(item['vertical_thumnail_url']),
            'description': mcpack.STR(item['description']),
            'author': mcpack.STR(item['author']),
            'link': mcpack.STR(item['link']),
            'block': mcpack.STR(item['block']),
            'play_count': mcpack.INT32(item['play_count']),
            'comment_count': mcpack.INT32(item['comment_count']),
            'up_count': mcpack.INT32(item['up_count']),
            'down_count': mcpack.INT32(item['down_count']),
            'pub_time': mcpack.INT32(item['pub_time']),
            'site': mcpack.STR(item['site']),
            'duration': mcpack.INT32(item['duration']),
            'real_link': mcpack.STR(item['real_link']),
            'hd': mcpack.INT32(item['hd']),
        }
        mcpack_body = mcpack.dumps(body)
        ##@head
        head = nshead.NsHead()
        head.body_len = len(mcpack_body)

        #2. connect to server
        #server_sock.create_connection((ip, port))
        server_sock.connect((ip, port))
        server_sock.settimeout(60)

        #3. send request
        request = head.pack() + mcpack_body
        server_sock.sendall(request)

        #4. recv response
        #parse response
        ret = 0
        resp_code = 200
        resp_content = "send success"
    except Exception as ex:
        ret = -1
        resp_code = -1
        resp_content = "Exception:%s" % ex
    finally:
        #5. disconnect with server
        server_sock.close()
    return ret, resp_code, resp_content
