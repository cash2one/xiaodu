# -*- coding: gbk -*-
import urllib2
from StringIO import StringIO
import gzip
import zlib



class Crawler:
    def __init__(self, timeout=20):
        self.timeout = timeout
        self._headers = {}

    def add_headers(self, headers_dict):
        for k, v in headers_dict.iteritems():
            self._headers[k] = v

    @staticmethod
    def decode_html_page(page):
        if isinstance(page, unicode):
            return page
        if not isinstance(page, str) or not page:
            return None
        start = page.find('charset=')
        if start != -1:
            start += len('charset=')
            if page[start] == '"': start += 1  # [charset="gbk"] in ku6.com
            end_i = page.find('"', start)
            if end_i != -1 and start < end_i:
                code_str = page[start:end_i].strip().lower()
                if code_str == 'utf8' or code_str == 'utf-8':
                    page_decode = page.decode('utf8', 'ignore')
                    return page_decode
                elif code_str == 'gbk':
                    page_decode = page.decode('gbk', 'ignore')
                    return page_decode
                elif code_str == 'gb2312':
                    page_decode = page.decode('gb2312', 'ignore')
                    return page_decode
        try:
            page_decode = page.decode('gbk')
        except UnicodeError:
            page_decode = page.decode('utf8')
        return page_decode

    def get_page(self, url):
        """
        抓取html页面，返回页面的内容(Unicode编码)
        """
        opener = urllib2.build_opener()
        http_req = urllib2.Request(url)
        for k, v in self._headers.iteritems():
            http_req.add_header(k, v)
        try:
            resp = opener.open(http_req, timeout=20)
            ce = resp.info().get('Content-Encoding')
            if ce and ce.lower() == 'gzip':
                buf = StringIO(resp.read())
                f = gzip.GzipFile(fileobj=buf)
                page = f.read()
            elif ce and ce.lower() == 'deflate':
                page = zlib.decompressobj(-zlib.MAX_WBITS).decompress(resp.read())
            else:
                page = resp.read()
        except urllib2.HTTPError as e:
            ce = e.info().get('Content-Encoding')
            if ce and ce.lower() == 'gzip':
                buf = StringIO(e.read())
                f = gzip.GzipFile(fileobj=buf)
                page = f.read()
            elif ce and ce.lower() == 'deflate':
                page = zlib.decompressobj(-zlib.MAX_WBITS).decompress(resp.read())
            else:
                raise e
        return resp.getcode(), resp.geturl(), dict(resp.info()), page


