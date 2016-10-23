# -*- coding: GBK -*-
import logging
import traceback
import request
import os
import urlparse
import re

unicodepoint = re.compile(u'\\\\u([0-9a-fA-F]{4})')
unicodepoint2 = re.compile(u'%u([0-9a-fA-F]{4})')


def unicode_replace(match):
    # print(match.group(1))
    return unichr(int(match.group(1), 16))


def decode_html_page(req):
    if len(req.body_decode) > 0:
        return
    if isinstance(req.body, unicode):
        req.body_decode = req.body
        return
    _decode_html_page(req)
    if req.body_decode:
        req.body_decode = unicodepoint.sub(unicode_replace, req.body_decode)


def _decode_html_page(req):
    # TO REMOVE
    # req = request.Request()
    ct = req.headers.get(u'content-type')
    if ct:
        ct = ct.lower()
        if u'utf8' in ct or u'utf-8' in ct:
            logging.info('decode page [h encoding: utf8]')
            req.body_decode = req.body.decode('utf8', 'ignore')
            return
        elif u'gbk' in ct:
            logging.info('decode page [h encoding: gbk]')
            req.body_decode = req.body.decode('gbk', 'ignore')
            return
        elif u'gb2312' in ct:
            logging.info('decode page [h encoding: gb2312]')
            req.body_decode = req.body.decode('gb2312', 'ignore')
            return
    start = req.body.find('charset=')
    if start != -1:
        start += len('charset=')
        if req.body[start] == '"': start += 1  # [charset="gbk"] in ku6.com
        end_i = req.body.find('"', start)
        if end_i != -1 and start < end_i:
            code_str = req.body[start:end_i].strip().lower()
            if code_str == 'utf8' or code_str == 'utf-8':
                logging.info('decode page [encoding: utf8]')
                req.body_decode = req.body.decode('utf8', 'ignore')
                return
            elif code_str == 'gbk':
                logging.info('decode page [encoding: gbk]')
                req.body_decode = req.body.decode('gbk', 'ignore')
                return
            elif code_str == 'gb2312':
                logging.info('decode page [encoding: gb2312]')
                req.body_decode = req.body.decode('gb2312', 'ignore')
                return
    try:
        logging.info('try to decode page using gbk')
        req.body_decode = req.body.decode('gbk')
    except UnicodeError:
        try:
            logging.info('try to decode page using utf8')
            req.body_decode = req.body.decode('utf8')
        except:
            logging.warning(traceback.format_exc())

def need_crawl_next(req):
    # TO REMOVE
    # req = request.Request()
    if req.http_code / 100 != 3:
        return None
    location = req.headers.get(u'location')
    if location is None: return None
    if location[0:7] != u'http://' and location[0:8] != u'https://':
        location_new = urlparse.urljoin(req.cur_url, location)
        logging.info('rebase location [%s] -> [%s]' % (location, location_new))
        if location_new == req.target_url or location_new == req.cur_url:
            return None
        req.headers[u'location'] = location_new
    resp = req.get_resp()
    resp.code, resp.msg = request.code_msg.get(u'need_crawl')
    resp.next_url = req.headers.get(u'location')
    resp.http_method = u'get'
    resp.is_asyn = False
    return resp

def clean_dir(dir_str, prefix_str, num):
    '''
    用于清理日志文件, 只保留 num 个文件
    :param dir_str: 日志文件的路劲
    :param prefix_str: 日志文件的前缀
    :param num: 只保留 num 个文件
    '''
    files = os.listdir(dir_str)
    tmp = list()
    for f in files:
        if prefix_str in f:
            tmp.append(f)
    files = sorted(tmp, reverse=True)
    for f in files[num:]:
        file_p = dir_str + os.sep + f
        logging.info('remove %s' % file_p)
        # print('remove %s' % file_p)
        os.remove(file_p)