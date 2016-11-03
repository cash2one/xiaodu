# -*- coding: GBK -*-
__metaclass__ = type
import re
import dc_req_pb2

http_code_pat = re.compile(r'http/[0-9]\.[0-9]\s*?([0-9]+)\s*?', flags=re.IGNORECASE)
code_msg = {
    u"live": (0, u"live url"),
    u"need_crawl": (0, u'need crawl page'),
    u"no_support": (0, u'url not support'),
    u"asyn_no_support": (0, u'asyn url no support'),
    u"decode_page_err": (0, u'decode page error'),
    u"r_t_h_p": (10, u"redirect to home page"),
    u"url_match": (11, u"url match [%s]"),
    u"redirect_url_match": (12, u"redirect url match [%s]"),
    u"title_match": (13, u"title match [%s]"),
    u"body_match": (14, u"body match [%s]"),
    u"little_body": (15, u"little body len[=%d]"),
    u"http_match": (24, u"http match [%s]"),
    u"http_4xx": (25, u"http %d"),  # http 4xx
    u"http_5xx": (26, u"http %d"),  # http 5xx
    u"http_3xx": (29, u"http %d"),  # http 3xx
    u"asyn_body_match": (30, u"asyn body match [%s]"),
    u"asyn_little_body": (31, u"asyn little body len[=%d]"),
    u"asyn_http_match": (34, u"asyn http match [%s]"),
    u"asyn_http_4xx": (35, u"asyn http %d"),  # http 4xx
    u"asyn_http_5xx": (36, u"asyn http %d"),  # http 5xx
    u"asyn_http_3xx": (39, u"asyn http %d"),  # http 3xx
}

class Request(object):
    def __init__(self):
        self.req_id = 0
        self.from_type = 0
        self.is_asyn = False
        self.is_relive = False
        self.target_url = u''      # 待检测的url
        self.cur_url = u''         # 抓取回来的网页对应的url(在发生跳转的情况下与target_url不同)
        self.user_data = None
        self.http_code = -1
        self.headers = dict()
        self.body = ''
        self.body_decode = u''
        self.no_resp = False
        self.resp_dest = u''
        self.check_level = u'normal'  # low, normal, high
        self.check_method = [u'http', u'link', u'title', u'body']

    def __str__(self):
        str_list = list()
        str_list.append(u'req_id: %s' % unicode(self.req_id))
        str_list.append(u'from_type: %s' % unicode(self.from_type))
        str_list.append(u'is_asyn: %s' % unicode(self.is_asyn))
        str_list.append(u'is_relive: %s' % unicode(self.is_relive))
        str_list.append(u'target_url: %s' % unicode(self.target_url))
        str_list.append(u'cur_url: %s' % unicode(self.cur_url))
        str_list.append(u'http_code: %s' % unicode(self.http_code))
        str_list.append(u'headers: %s' % unicode(self.headers))
        str_list.append(u'no_resp: %s' % unicode(self.no_resp))
        str_list.append(u'resp_dest: %s' % unicode(self.resp_dest))
        str_list.append(u'check_level: %s' % unicode(self.check_level))
        str_list.append(u'check_method: %s' % u'|'.join(self.check_method))
        str_list.append(u'len(user_data): %d' % len(self.user_data))
        str_list.append(u'len(body): %d' % len(self.body))
        return u'\n'.join(str_list).encode('gbk')

    def set_http_code(self, status_line):
        m = http_code_pat.search(status_line)
        if m:
            self.http_code = int(m.group(1))

    def set_headers(self, headers_str):
        """
        把字符串格式 headers 转换为dict， headers格式 key1:value1 \r\n key2:value2 \r\n
        """
        if not isinstance(headers_str, str) and not isinstance(headers_str, unicode):
            raise TypeError
        headers_str = unicode(headers_str)
        ent = headers_str.split(u'\r\n')
        for header_str in ent:
            header_str = header_str.strip()
            if header_str:
                self.add_header(header_str)

    def add_header(self, header_str):
        """
        把 key : vaule 格式的字符串添加到 headers 字典中
        """
        if not isinstance(header_str, str) and not isinstance(header_str, unicode):
            raise TypeError
        header_str = unicode(header_str)
        ent = header_str.split(':', 1)
        if len(ent) != 2:
            return
        self.headers[ent[0].strip().lower()] = ent[1].strip()

    @staticmethod
    def from_proto_req(p_req):
        req = Request()
        req.req_id, req.from_type = p_req.req_id, p_req.from_type
        req.is_asyn, req.is_relive = p_req.is_asyn, p_req.is_relive
        req.no_resp = p_req.no_resp
        req.target_url, req.cur_url = p_req.target_url, p_req.cur_url
        req.user_data = p_req.user_data
        req.http_code, req.body = p_req.http_code, p_req.body
        req.set_headers(p_req.headers)
        req.resp_dest = p_req.resp_dest
        if p_req.check_level == dc_req_pb2.NORMAL:
            req.check_level = u'normal'
        elif p_req.check_level == dc_req_pb2.LOW:
            req.check_level = u'low'
        elif p_req.check_level == dc_req_pb2.HIGH:
            req.check_level = u'high'
        if len(p_req.check_methods) > 0:
            req.check_method = list()
            for cm in p_req.check_methods:
                if cm == dc_req_pb2.HTTP:
                    req.check_method.append(u'http')
                elif cm == dc_req_pb2.LINK:
                    req.check_method.append(u'link')
                elif cm == dc_req_pb2.TITLE:
                    req.check_method.append(u'title')
                elif cm == dc_req_pb2.BODY:
                    req.check_method.append(u'body')
        return req

    @staticmethod
    def from_mcpack_req(m_req):
        req = Request()
        tmp = m_req.get('req_id')
        if tmp is not None: req.req_id = int(tmp)
        tmp = m_req.get('from_type')
        if tmp is not None: req.from_type = int(tmp)
        tmp = m_req.get('is_asyn')
        if tmp is not None: req.is_asyn = bool(tmp)
        tmp = m_req.get('is_relive')
        if tmp is not None: req.is_relive = bool(tmp)
        tmp = m_req.get('no_resp')
        if tmp is not None: req.no_resp = bool(tmp)
        tmp = m_req.get('target_url')
        if tmp is not None: req.target_url = str(tmp).decode('gbk')
        tmp = m_req.get('cur_url')
        if tmp is not None: req.cur_url = str(tmp).decode('gbk')
        tmp = m_req.get('user_data')
        if tmp is not None: req.user_data = tmp
        tmp = m_req.get('http_code')
        if tmp is not None: req.http_code = int(tmp)
        tmp = m_req.get('headers')
        if tmp is not None:
            req.set_headers(str(tmp).decode('gbk'))
        tmp = m_req.get('body')
        if tmp is not None: req.body = tmp
        tmp = m_req.get('resp_dest')
        if tmp is not None: req.resp_dest = str(tmp).decode('gbk')
        tmp = m_req.get('check_level')
        if tmp is not None: req.check_level = str(tmp).decode('gbk')
        tmp = m_req.get('check_methods')
        if tmp is not None: req.check_method = str(tmp).decode('gbk').split(u'|')
        return req

    def get_resp(self):
        """
        返回和该 req 对应的 resp
        """
        resp = _Response()
        resp.req_id = self.req_id
        resp.cur_url = self.cur_url
        resp.target_url = self.target_url
        # resp.no_resp = self.no_resp
        resp.resp_dest = self.resp_dest
        resp.user_data = self.user_data
        return resp


class _Response(object):
    def __init__(self):
        self.code = 0
        self.msg = u'live url'
        self.req_id = 0
        self.is_asyn = False
        self.cur_url = self.target_url = self.next_url = u''
        # self.no_resp = False
        self.resp_dest = u''
        self.http_method = u'get'
        self.user_data = None

    def __str__(self):
        ret_str = "[req_id: %d, resp_dest: %s, code: %d, msg: %s, target_url: %s, cur_url: %s, next_url: %s]"
        return ret_str % (self.req_id, self.resp_dest, self.code, self.msg, self.target_url, self.cur_url, self.next_url)

    def to_proto_req(self, p_resp):
        p_resp.code = self.code
        p_resp.msg = self.msg
        p_resp.req_id = self.req_id
        p_resp.is_asyn = self.is_asyn
        p_resp.cur_url = self.cur_url
        p_resp.target_url = self.target_url
        p_resp.next_url = self.next_url
        if self.http_method == u'get':
            p_resp.http_method = dc_req_pb2.GET
        elif self.http_method == u'head':
            p_resp.http_method = dc_req_pb2.HEAD
        elif self.http_method == u'post':
            p_resp.http_method = dc_req_pb2.POST
        p_resp.resp_dest = self.resp_dest
        p_resp.user_data = self.user_data


def test():
    m = http_code_pat.search('HTTP/1.1 200 Connection established\r\nVia: 1.1 USA-ITE-CAS01')
    if m:
        print(m.group(1))
    m = http_code_pat.search('HTTP/1.1 200 Connection established\r\n')
    if m:
        print(m.group(1))

if __name__ == '__main__':
    test()
