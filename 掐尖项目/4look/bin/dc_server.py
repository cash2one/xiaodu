# -*- coding: GBK -*-
from __future__ import print_function
__metaclass__ = type
# import mcpack
import nshead
import logging
import codecs
import sys
import argparse
import socket
import os
import traceback
from dc import dc, request, util
from dc import dc_req_pb2
from datetime import datetime

cur_hour = None
output_dir = None
output_file_prefix = 'indexdb.data.'
relive_output_file_prefix = 'relive.data.'
output_f = None
relive_output_f = None
exit_count = 0
max_exit_count = 500000


def create_output_per_hour():
    global cur_hour, output_f, relive_output_f
    now_hour = datetime.now().strftime('%Y%m%d%H')
    if cur_hour is None or now_hour != cur_hour:
        util.clean_dir(output_dir, output_file_prefix, 10)
        util.clean_dir(output_dir, relive_output_file_prefix, 10)
        cur_hour = now_hour
        if output_f:
            output_f.close()
        if relive_output_f:
            relive_output_f.close()
        output_f = codecs.open(output_dir + os.sep + output_file_prefix + cur_hour + '.txt',
                               mode='ab', encoding='gbk', errors='ignore')
        relive_output_f = codecs.open(output_dir + os.sep + relive_output_file_prefix + cur_hour + '.txt',
                                      mode='ab', encoding='gbk', errors='ignore')

def cs_process(s, my_dc):
    global exit_count
    data = ""
    while True:
        create_output_per_hour()
        while len(data) < nshead.head_size:
            new_read = s.recv(4096)
            data += new_read
            if len(new_read) == 0:
                return
        head = data[0:nshead.head_size]
        ns = nshead.NsHead()
        ns.unpack(head)
        data = data[nshead.head_size:]
        while len(data) < ns.body_len:
            new_read = s.recv(4096)
            data += new_read
            if len(new_read) == 0:
                logging.info("_read_pack_: client close socket")
                return
        body = data[0: ns.body_len]
        data = data[len(body):]
        if ns.id == 10:
            logging.info('reload config')
            my_dc.reload_conf()
            continue
        # mc_dict = mcpack.loads(body)
        proto_req = dc_req_pb2.request()
        proto_req.ParseFromString(body)
        logging.info('--------------  count : %d ------------' % exit_count)

        req = request.Request.from_proto_req(proto_req)
        logging.info('begin check: [target_url: %s, cur_url: %s]' % (req.target_url, req.cur_url))
        logging.debug(req)
        try:
            resp = my_dc.judge(req)
            proto_resp = dc_req_pb2.response()
            resp.to_proto_req(proto_resp)
            # log something to database
            if req.is_relive:
                relive_output_f.write('%s\t%s\t%d\t%s\n' % (req.target_url, req.target_url, resp.code, resp.msg))
            else:
                output_f.write('%s\t%s\t%d\t%s\n' % (req.target_url, req.target_url, resp.code, resp.msg))
            if not req.no_resp:
                binary = proto_resp.SerializeToString()
                ns = nshead.NsHead()
                ns.body_len = len(binary)
                ns_binary = ns.pack()
                logging.info('send result to socket [%s:%d]\n' % s.getpeername())
                s.sendall(ns_binary + binary)
        except:
            print('--------- %s [%s]-------------' % (datetime.now(), req.target_url), file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            continue
        exit_count += 1
        if exit_count > max_exit_count:
            s.close()
            return


def main():
    global output_dir
    parser = argparse.ArgumentParser(description='dead link check server')
    parser.add_argument('-p', '--port', nargs='?', type=int, required=True, dest='port', help='server port')
    parser.add_argument('--logdir', nargs='?', type=str, required=True, help='log file directory')
    parser.add_argument('--outputdir', nargs='?', type=str, required=True, help='output file directory')
    parser.add_argument('--confdir', nargs='?', type=str, default='./conf', help='conf file director')
    args = parser.parse_args()
    log_dir = args.logdir
    output_dir = args.outputdir
    conf_dir = args.confdir
    PORT = args.port

    log_file = log_dir + os.sep + 'dc_server.log'
    if os.access(log_file, os.F_OK) and os.stat(log_file).st_size:
        os.rename(log_file, log_file+'.'+datetime.now().strftime('%m%d%H%M'))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # or whatever
    handler = logging.FileHandler(log_file, 'w', 'gbk')  # or whatever
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))  # or whatever
    root_logger.addHandler(handler)

    util.clean_dir(log_dir, 'dc_server.log.', 5)

    # add database configure here
    my_dc = dc.DC(conf_dir, db_conf=dict(), check_conf_change=True, debug=True)

    server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_s.bind(("", PORT))
    server_s.listen(8)
    while True:
        cli_s, _ = server_s.accept()
        if cli_s is None: continue
        logging.info('accept a connect from [%s:%d]' % cli_s.getpeername())
        try:
            cs_process(cli_s, my_dc)
        except Exception as e:
            logging.warning(traceback.format_exc())
            logging.warning(e)
            cli_s.close()
        logging.info('connection closed')
        if exit_count > max_exit_count:
            break
    logging.info('have process %d requests, bye bye...' % exit_count)
    sys.exit(-1)


if __name__ == "__main__":
    main()

