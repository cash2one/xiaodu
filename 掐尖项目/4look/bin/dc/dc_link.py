# -*- coding: GBK -*-
import conf
import request
import logging
import urlparse
import util


def _is_home_page(url):
    ent = url.split(u'/')
    if len(ent) <= 3:
        return True
    if len(ent) == 4:
        if len(ent[3]) == 0:
            return True
        if ent[3] == u'index' or ent[3] == u'index.html' or ent[3] == u'index.shtml' or ent[3] == u'index.php':
            return True
    return False


def _home_page_resp(req):
    err, msg = request.code_msg.get(u'r_t_h_p')
    resp = req.get_resp()
    resp.code, resp.msg = err, msg
    logging.info('find dead: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                 (req.target_url, req.cur_url, resp.code, resp.msg))
    return resp


def judge(site_conf, req):
    # TO REMOVE
    # req = request.Request()
    if req.cur_url and req.target_url != req.cur_url:
        for rule in site_conf.rules:
            if isinstance(rule, conf.SiteConf.Rule) and rule.method == u'link':
                ret = rule.check_match(req.cur_url)
                if ret:
                    err, msg = request.code_msg.get(u'url_match')
                    resp = req.get_resp()
                    resp.code = err
                    resp.msg = msg % rule.match_str()
                    logging.info('find dead: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                                 (req.target_url, req.cur_url, resp.code, resp.msg))
                    return resp
        if _is_home_page(req.cur_url):
            return _home_page_resp(req)
        # return req.get_resp()
    if req.http_code < 0:
        logging.error('do not init http code, please init it')
        return req.get_resp()
    hc = req.http_code / 100
    location = req.headers.get(u'location')
    if hc != 3 or not location:
        return req.get_resp()
    # some server response Relative URL, so need to rebase it
    if location[0:7] != u'http://' and location[0:8] != u'https://':
        location_new = urlparse.urljoin(req.cur_url, location)
        logging.info('rebase location [%s] -> [%s]' % (location, location_new))
        location = location_new
    for rule in site_conf.rules:
        if isinstance(rule, conf.SiteConf.Rule) and rule.method == u'link':
            ret = rule.check_match(location)
            if ret:
                err, msg = request.code_msg.get(u'redirect_url_match')
                resp = req.get_resp()
                resp.code = err
                resp.msg = msg % rule.match_str()
                logging.info('find dead: [target_url:%s][cur_url:%s] code: %d, msg: %s' %
                             (req.target_url, req.cur_url, resp.code, resp.msg))
                return resp
    if _is_home_page(location):
        return _home_page_resp(req)
    resp = util.need_crawl_next(req)
    if resp is not None:
        logging.info('need_crawl: [target_url:%s][next_url:%s, http_method: %s] code: %d, msg: %s' %
                     (req.target_url, resp.next_url, resp.http_method, resp.code, resp.msg))
        return resp
    return req.get_resp()
