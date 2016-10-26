#encoding: utf-8
 
'''
*
* @file app.py
* @author wangshuxiang_vd(com@baidu.com)
* @date 2016/08/19 16:34:38
* @brief 
**/
'''

import sys
#set encode
reload(sys)
sys.setdefaultencoding("utf-8")
#set path
sys.path.append("./lib")

import logging
import traceback
import tornado.web
from tornado import gen
from concurrent.futures import ThreadPoolExecutor
import socket
import nshead
import mcpack

#video class handler
def handle(req_type, text):
    #ret infomation
    ret = 0
    resp_code = 0
    resp_content = "xxx"
    #video_class server
    ip = "127.0.0.1"
    port = 9875
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #1.build request pack
        ##@content
        body = {
            'request_type' : mcpack.INT32(req_type),
            'text' : mcpack.STR(text)
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
        res_nshead = nshead.NsHead.from_str(server_sock.recv(36))
        if res_nshead is False:
            return -3, -1, "text is invalid"
        recved = 0
        body = ''
        while recved < res_nshead.body_len:
            temp = server_sock.recv(1024)
            recved += len(temp)
            body = body + temp
        res_body = mcpack.loads(body)
        #parse response
        resp_code = res_body['response_code']
        resp_content = res_body['tags']
    except Exception as ex:
        ret = -1
        resp_code = -1
        resp_content = "maybe error in param!"
        logging.error(traceback.format_exc())
    finally:
        #5. disconnect with server
        server_sock.close()
    return ret, resp_code, resp_content

##run app
if __name__ == "__main__":
    #init log
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    #test
    req_type = 1 # 0:query, 1:title
    text = "搞笑的电视剧"
    ret, code, resp = handle(req_type, text)
    print ret, code, resp
