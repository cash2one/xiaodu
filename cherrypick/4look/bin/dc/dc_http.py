# -*- coding: GBK -*-
import conf
import request
import logging
import util


def judge(site_conf, req, is_asyn=False):
    # TO REMOVE
    # req = req.Request()
    if req.http_code < 0:
        logging.error('do not init http code, please init it')
        return req.get_resp()
    is_hava_http_rule = False
    for rule in site_conf.rules:
        if isinstance(rule, conf.SiteConf.Rule) and rule.method == u'http':
            is_hava_http_rule = True
            ret = rule.check_match(str(req.http_code))
            if ret:
                if is_asyn:
                    err, msg = request.code_msg.get(u'asyn_http_match')
                else:
                    err, msg = request.code_msg.get(u'http_match')
                resp = req.get_resp()
                resp.code = err
                resp.msg = msg % rule.match_str()
                logging.info('find dead: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                             (req.target_url, req.cur_url, resp.code, resp.msg))
                return resp
    if is_hava_http_rule:   # 如果有配 http 的 rule, 则不走默认的 http策略
        return req.get_resp()
    hc = req.http_code / 100
    err, msg = 0, u''
    if hc == 3:
        resp = util.need_crawl_next(req)
        if resp is not None:
            # logging.info('need_crawl: [target_url:%s][next_url:%s, http_method: %s] code: %d, msg: %s' %
            #              (req.target_url, resp.next_url, resp.http_method, resp.code, resp.msg))
            return resp
    elif hc == 4:
        if is_asyn:
            err, msg = request.code_msg.get(u'asyn_http_4xx')
        else:
            err, msg = request.code_msg.get(u'http_4xx')
    elif hc == 5:
        if is_asyn:
            err, msg = request.code_msg.get(u'asyn_http_5xx')
        else:
            err, msg = request.code_msg.get(u'http_5xx')

    if err != 0:
        # msg = err_msg[1] % err_msg[0]
        resp = req.get_resp()
        resp.msg = msg % req.http_code
        # 大部分情况下, 5xx 的页面是可以播放的，为了减少误判，把 5xx 当成活链
        if req.http_code == 403 or hc == 5:
            resp.code = 0
            logging.info('find live: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                         (req.target_url, req.cur_url, resp.code, resp.msg))
        else:
            resp.code = err
            logging.info('find dead: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                         (req.target_url, req.cur_url, resp.code, resp.msg))
        return resp
    else:
        return req.get_resp()
