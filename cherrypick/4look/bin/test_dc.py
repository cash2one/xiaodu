# -*- coding: GBK -*-
import socket
import requests
import logging
import nshead
from dc import dc_req_pb2
import sys
import codecs
import os
import time

class DCClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = int(server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))

    def create_req(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        print('get %s' % url)
        r = requests.get(url, allow_redirects=False, headers=headers)
        logging.info('%s %s %d %s' % (r.status_code, r.url, len(r.text), r.headers))
        req = dc_req_pb2.request()
        req.req_id = 22
        req.from_type = 88
        req.is_relive = False
        req.is_asyn = False
        req.no_resp = False
        req.check_level = dc_req_pb2.NORMAL
        req.check_methods.append(dc_req_pb2.HTTP)
        req.check_methods.append(dc_req_pb2.LINK)
        req.check_methods.append(dc_req_pb2.TITLE)
        req.check_methods.append(dc_req_pb2.BODY)
        req.target_url = url
        req.cur_url = r.url
        req.http_code = r.status_code
        header_list = list()
        for k, v in r.headers.iteritems():
            header_list.append(u'%s: %s' % (k.strip(), v.strip()))
        req.headers = u'\r\n'.join(header_list) + u'\r\n'
        req.body = r.content
        req.resp_dest = u''
        req.user_data ='{"hello": "world"}'
        # logging.debug(req)
        return req

    def send_req(self, req):
        binary = req.SerializeToString()
        ns = nshead.NsHead()
        ns.body_len = len(binary)
        ns_binary = ns.pack()
        logging.info('send req to server [%s:%d][body_len: %d]' % (self.sock.getpeername()[0],self.sock.getpeername()[1], ns.body_len))
        self.sock.sendall(ns_binary + binary)
        logging.info('wait for server resp ......')
        data = ""
        while len(data) < nshead.head_size:
            new_read = self.sock.recv(nshead.head_size - len(data))
            data += new_read
            if len(new_read) == 0:
                logging.warning('server close the socket[len(data) = %d]' % len(data))
                return None

        head = data[0:nshead.head_size]
        ns = nshead.NsHead()
        ns.unpack(head)
        data = data[nshead.head_size:]
        while len(data) < ns.body_len:
            new_read = self.sock.recv(ns.body_len - len(data))
            data += new_read
            if len(new_read) == 0:
                logging.warning('server close the socket[len(data) = %d]' % len(data))
                return None
        resp = dc_req_pb2.response()
        resp.ParseFromString(data[ : ns.body_len])
        return resp

    def test(self, url):
        req = self.create_req(url)
        resp = self.send_req(req)
        logging.info(resp)
        while len(resp.next_url) > 0:
            req2 = self.create_req(resp.next_url)
            req2.target_url = req.target_url
            req2.is_asyn = resp.is_asyn
            resp = self.send_req(req2)
            logging.info(resp)
        return resp

    def server_reload_conf(self):
        ns = nshead.NsHead()
        ns.id = 10
        ns.body_len = 0
        logging.info('send server reload conf req to server')
        self.sock.sendall(ns.pack())

def run():
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    dcc = DCClient('localhost', 8080)
    # dcc.test('http://www.iqiyi.com/v_19rroopf0k.html')
    # dcc.test('http://www.iqiyi.com/v_19rroopf0ka.html')
    # dcc.test('http://www.aipai.com/x17/PzYgJiElJiRqJWQhKQ.html')
    # dcc.test('http://www.56.com/u37/v_MTE3ODg4MDgy.html')
    # dcc.test('http://v.youku.com/v_show/id_XNjM1MjUxNzU2.html')
    # dcc.test('http://video.baomihua.com//30894844')
    # dcc.test('http://vod.kankan.com/v/68/68985/279317.shtml?id=731032')
    # dcc.test('http://vod.kankan.com/v/88/88747/483800.shtml')
    # dcc.test('http://v.pps.tv/play_36TBQ8.html#from_baidu')
    # dcc.test('http://v.ku6.com/show/XQBegQE1JC5C1rw7SNnS1A...htm')
    # dcc.test('http://www.fun.tv/vplay/v-3650276')
    # dcc.server_reload_conf()
    # dcc.test('http://www.hunantv.com/v/3/41696/f/473134.html')
    # dcc.test('http://v.youku.com/v_show/id_XNzI0OTM1MjYw.html')
    dcc.test('http://www.funshion.com/video/play/101680/')

def run_file():
    # if len(sys.argv) != 3:
    #     print('Usage: %s <input.txt> <output.txt>' % sys.argv[0])
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # or whatever
    handler = logging.FileHandler('test' + os.sep + 'test_dc.log', 'w', 'gbk')  # or whatever
    handler.setFormatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')  # or whatever
    root_logger.addHandler(handler)
    in_f = codecs.open('test' + os.sep + 'input.txt', encoding='gbk')
    out_f = codecs.open('test' + os.sep + 'output.txt', encoding='gbk', mode='w')
    dcc = DCClient('localhost', 8080)
    while True:
        line = in_f.readline()
        if not line: break
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue
        resp = dcc.test(line)
        if resp is not None:
            out_f.write('%s\t%d\t%s\n' %(resp.target_url.decode('gbk'), resp.code, resp.msg.decode('gbk')))
    in_f.close()
    out_f.close()

def server_reload_conf():
    dcc = DCClient('localhost', 8080)
    dcc.server_reload_conf()



if __name__ == '__main__':
    run()




