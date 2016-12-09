# -*- coding: GBK -*-
import conf
import mysql.connector
import logging
import traceback
import request
import util
import re
import dc_link
import dc_http
import sys
reload(sys)
sys.path.append("./pyspider/pyspider-0.3.8/pyspider/libs/bin/dc")
class DC:
    def __init__(self, conf_dir, db_conf=dict(), check_conf_change=False, debug=False):
        self._conf_dir = conf_dir
        self._db_conf = dict()
        self._db_conf.update(db_conf)
        self._check_conf_change = check_conf_change
        self._debug = debug
        self._title_pat = re.compile(ur'<title>(.+?)</title>', flags=re.IGNORECASE)
        self._conf = conf.Conf(self._conf_dir, 'page_judge.conf', 'asyn_judge.conf')
        self._conn = None
        self.db_conn()

    def db_conn(self):
        try:
            if self._db_conf is not None and isinstance(self._db_conf, dict) and len(self._db_conf) > 0:
                self._conn = mysql.connector.connect(**self._db_conf)
        except:
            logging.error(traceback.format_exc())
            self._conn = None

    def reload_conf(self):
        self._conf.reload_conf()

    def judge(self, req):
        # TO REMOVE
        # req = request.Request()
        if req.cur_url is None or len(req.cur_url) == 0 \
                or not req.is_asyn and len(req.body) == 0 and req.http_code == -1:
            resp = req.get_resp()
            resp.code, resp.msg = request.code_msg.get(u'need_crawl')
            resp.next_url = resp.target_url
            logging.warning('need_crawl: [target_url:%s][next_url:%s, http_method:%s] code: %d, msg: %s' %
                            (req.target_url, resp.next_url, resp.http_method, resp.code, resp.msg))
            return resp
        # elif req.is_asyn and len(req.body) == 0:
        #     # TODO: 播放器死链，还未实现
        #     return req.get_resp()
        elif req.is_asyn:
            # 对异步页面的检测
            logging.info('do async judge [target_url:%s][cur_url:%s]' % (req.target_url, req.cur_url))
            return self._judge_async(req)
        else:
            # 普通页面死链检测
            logging.info('do page judge [target_url:%s][cur_url:%s]' % (req.target_url, req.cur_url))
            return self._judge_body(req)

    def _judge_async(self, req):
        for async_conf in self._conf.asyn_temp:
            # TO REMOVE
            # async_conf = conf.AsynConf('', '')
            if async_conf.page_regex.match(req.cur_url):
                have_body, have_http, have_link, have_title = self._check_method(req, async_conf.method)
                resp = req.get_resp()
                if have_http:
                    logging.info('judge by async http code')
                    resp = dc_http.judge(async_conf, req, is_asyn=True)
                    if resp.code != 0:
                        return resp
                    # if resp.code == 0 and len(resp.next_url) > 0 and not have_link:
                    if resp.code == 0 and len(resp.next_url) > 0:
                        logging.info('need_crawl: [target_url:%s][next_url:%s, http_method: %s] code: %d, msg: %s' %
                                    (req.target_url, resp.next_url, resp.http_method, resp.code, resp.msg))
                        return resp
                if have_body:
                    logging.info('judge by page')
                    util.decode_html_page(req)
                    if req.body_decode is None or (len(req.body_decode) == 0 and len(req.body) > 0):
                        resp = req.get_resp()
                        err, msg = request.code_msg.get(u'decode_page_err')
                        resp.code, resp.msg = err, msg
                        logging.info('find live:  [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                                     (req.target_url, req.cur_url, resp.code, resp.msg))
                        return resp
                    for rule in async_conf.rules:
                        if not isinstance(rule, conf.SiteConf.Rule):
                            continue
                        if rule.method == u'body':
                            if rule.check_match(req.body_decode):
                                if isinstance(rule.regex_list, int):
                                    err, msg = request.code_msg.get(u'asyn_little_body')
                                    msg %= len(req.body_decode)
                                else:
                                    err, msg = request.code_msg.get(u'asyn_body_match')
                                    msg %= rule.match_str()
                                resp = req.get_resp()
                                resp.code, resp.msg = err, msg
                                logging.info('find dead: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                                             (req.target_url, req.cur_url, resp.code, resp.msg))
                                return resp
                if resp is None:
                    resp = req.get_resp()
                for rule in async_conf.rules:
                    if isinstance(rule, conf.SiteConf.AsynRule):
                        util.decode_html_page(req)
                        params_dict = rule.generate_params_dict(req.target_url, req.body_decode)
                        if params_dict is not None:
                            resp.next_url = rule.url_format % params_dict
                            resp.http_method = rule.http_method
                            resp.is_asyn = True
                            resp.code, resp.msg = request.code_msg.get(u'need_crawl')
                            logging.info('need_crawl: [target_url:%s][next_url:%s, http_method: %s] code: %d, msg: %s' %
                                         (req.target_url, resp.next_url, resp.http_method, resp.code, resp.msg))
                            return resp
                logging.info('find live: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                             (req.target_url, req.cur_url, resp.code, resp.msg))
                return resp
        else:
            resp = req.get_resp()
            resp.code, resp.msg = request.code_msg.get(u'asyn_no_support')
            logging.warning('no support: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                            (req.target_url, req.cur_url, resp.code, resp.msg))
            return resp

    def _judge_body(self, req):
        site_conf = self._conf.get_site_conf(req.target_url)
        # TO REMOVE
        # site_conf = conf.SiteConf("","")
        if site_conf is None:
            resp = req.get_resp()
            resp.code, resp.msg = request.code_msg.get(u'no_support')
            logging.warning('no support: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                            (req.target_url, req.cur_url, resp.code, resp.msg))
            return resp

        have_body, have_http, have_link, have_title = self._check_method(req, site_conf.method)
        resp = req.get_resp()
        if have_http:
            logging.info('judge by http code')
            resp = dc_http.judge(site_conf, req)
            if resp.code != 0:
                return resp
            if resp.code == 0 and len(resp.next_url) > 0 and not have_link:
                logging.info('need_crawl: [target_url:%s][next_url:%s, http_method: %s] code: %d, msg: %s' %
                             (req.target_url, resp.next_url, resp.http_method, resp.code, resp.msg))
                return resp
        if have_link:
            logging.info('judge by link')
            resp = dc_link.judge(site_conf, req)
            if resp.code != 0:
                return resp
            elif resp.code == 0 and len(resp.next_url) > 0:
                return resp
        if have_title:
            logging.info('judge by title')
            util.decode_html_page(req)
            m = self._title_pat.search(req.body_decode)
            if m is not None:
                title = m.group(1)
                logging.info('title [%s]' % title)
                ###新增规则
                if title == u'—在线播放—优酷网，视频高清在线观看':
                    err, msg = request.code_msg.get(u'title_match')
                    resp = req.get_resp()
                    resp.code, resp.msg = err, msg
                    logging.info('find dead: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                                 (req.target_url, req.cur_url, resp.code, resp.msg))
                    return resp
                ###
                for rule in site_conf.rules:
                    if isinstance(rule, conf.SiteConf.Rule) and rule.method == u'title':
                        if rule.check_match(title):
                            err, msg = request.code_msg.get(u'title_match')
                            msg %= rule.match_str()
                            resp = req.get_resp()
                            resp.code, resp.msg = err, msg
                            logging.info('find dead: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                                         (req.target_url, req.cur_url, resp.code, resp.msg))
                            return resp
        if have_body:
            logging.info('judge by page')
            util.decode_html_page(req)
            if req.body_decode is None or len(req.body_decode) == 0:
                resp = req.get_resp()
                err, msg = request.code_msg.get(u'decode_page_err')
                resp.code, resp.msg = err, msg
                logging.info('find live:  [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                             (req.target_url, req.cur_url, resp.code, resp.msg))
                return resp
            for rule in site_conf.rules:
                if isinstance(rule, conf.SiteConf.Rule) and rule.method == u'body':
                    if rule.check_match(req.body_decode):
                        if isinstance(rule.regex_list, int):
                            err, msg = request.code_msg.get(u'little_body')
                            msg %= len(req.body_decode)
                        else:
                            err, msg = request.code_msg.get(u'body_match')
                            msg %= rule.match_str()
                        resp = req.get_resp()
                        resp.code, resp.msg = err, msg
                        logging.info('find dead: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                                     (req.target_url, req.cur_url, resp.code, resp.msg))
                        return resp
        if resp is None:
            resp = req.get_resp()
        if (req.check_level != u'low' and u'v.youku.com/' not in req.target_url \
                and u'www.tudou.com/' not in req.target_url and u'ku6.com/' not in req.target_url) or \
                (req.check_level == u'high'):
            for rule in site_conf.rules:
                if isinstance(rule, conf.SiteConf.AsynRule):
                    util.decode_html_page(req)
                    params_dict = rule.generate_params_dict(req.target_url, req.body_decode)
                    if params_dict is not None:
                        resp.next_url = rule.url_format % params_dict
                        resp.http_method = rule.http_method
                        resp.is_asyn = True
                        resp.code, resp.msg = request.code_msg.get(u'need_crawl')
                        logging.info('need_crawl: [target_url:%s][next_url:%s, http_method: %s] code: %d, msg: %s' %
                                     (req.target_url, resp.next_url, resp.http_method, resp.code, resp.msg))
                        return resp
        logging.info('find live: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                     (req.target_url, req.cur_url, resp.code, resp.msg))
        return resp

    @staticmethod
    def _check_method(req, methods):
        all_methods = (u'body', u'http', u'link', u'title')
        req_m = [False, False, False, False]
        conf_m = [False, False, False, False]
        for idx, m1 in enumerate(all_methods):
            for m2 in req.check_method:
                if m2 == m1:
                    req_m[idx] = True
        for idx, m1 in enumerate(all_methods):
            for m2 in methods:
                if m2 == m1:
                    conf_m[idx] = True
        return req_m[0] and conf_m[0], req_m[1] and conf_m[1], req_m[2] and conf_m[2], req_m[3] and conf_m[3]


def batch_test():
    import crawler
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    cc = crawler.Crawler()
    cc.add_headers({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    hc, url, header, page = cc.get_page('http://my.tv.sohu.com/us/241816781/80597444.shtml')
    logging.info('%s %s %s' % (hc, url, header))


fw = open('deadlinks.txt','a')
def dead_detect(target_url):
    import requests
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(target_url, allow_redirects=False, headers=headers)
    logging.info('%s %s %d %s' % (r.status_code, r.url, len(r.text), r.headers))
    mydc = DC("/home/video/dist_pyspider/pyspider/pyspider-0.3.8/pyspider/libs/dc")
    myreq = request.Request()
    myreq.http_code, myreq.headers, myreq.body = r.status_code, r.headers, r.content
    myreq.target_url, myreq.cur_url = target_url, r.url
    resp = mydc.judge(myreq)
    logging.info(resp)
    if resp.code != 0:
        fw.write(target_url+'\n')
        fw.flush()
    return  resp.code

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)
    #print dead_detect('http://www.iqiyi.com/dianshiju/20121002/1fcf6d6779536c7f.html')
    #print dead_detect('http://m.acfun.tv/v/?ac=31868')
    try:
        print dead_detect('https://www.le.com/ptv/vplay/00.html')
    except:
        print 'no'
    #print dead_detect('http://weibo.com/228074/E9uQnB5LA?ref=feedsdk&type=comment')
