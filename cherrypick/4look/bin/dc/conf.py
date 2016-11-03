# -*- coding: GBK -*-
__metaclass__ = type
import os
import codecs
import re
import logging
import urlparse
from datetime import datetime


"""
有两个配置文件： page_judge.conf 和 asyn_judge.conf
"""


class ConfError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return unicode(self.value)


class SiteConf(object):
    def __init__(self, site, methods_str):
        self.site = site
        self.page_regex_str = u''
        self.page_regex = None
        self.rules = list()
        if not methods_str or methods_str == u"*":
            methods_str = u'http|link|title|body'
        self.method = tuple(sorted(methods_str.split(ur'|')))

    def __str__(self):
        site_str_list = list()
        site_str_list.append(u'site\t%s\t%s' % (self.site, u'|'.join(self.method)))
        if self.page_regex is not None:
            site_str_list.append(u'\tpage_regex\t%s' % self.page_regex.pattern)
        map(lambda x: site_str_list.append(unicode(x)), self.rules)
        return u'\n'.join(site_str_list)

    def set_page_regex(self, page_regex):
        self.page_regex_str = page_regex
        self.page_regex = re.compile(self.page_regex_str)

    class Rule(object):
        def __init__(self, method, regex_list_str):
            self.method = method
            self.regex_list_str = regex_list_str
            ent = self.regex_list_str.split(u'\t')
            if self.method == u'body' and len(ent) == 2 and ent[0] == u'smallpage':
                self.regex_list = int(ent[1])
                return
            self.regex_list = self._create_regex_list()

        def check_match(self, text):
            if self.method == u'body' and isinstance(self.regex_list, int):
                return self.regex_list > len(text)
            bool_list = list()
            have_not = False
            for r in self.regex_list:
                if isinstance(r, bool):
                    have_not = True
                else:
                    m = r.search(text)
                    if have_not:
                        bool_list.append(not bool(m is not None))
                    else:
                        bool_list.append(bool(m is not None))
                    have_not = False
            for b in bool_list:
                if b is False:
                    return False
            return True

        def match_str(self):
            r_list = list()
            for r in self.regex_list:
                if isinstance(r, bool) and not r:
                    if len(r_list) > 0 and r_list[-1] != u'not':
                        r_list.append(u'and')
                    r_list.append(u'not')
                    continue
                if len(r_list) == 0 or r_list[-1] == u'not':
                    r_list.append(r)
                    continue
                r_list.append(u'and')
                r_list.append(r)
            for i, v in enumerate(r_list):
                if not isinstance(v, unicode):
                    r_list[i] = unicode(v.pattern)
            return u'\t'.join(r_list)

        def __str__(self):
            if self.method == u'body' and isinstance(self.regex_list, int):
                return u'\tbody\tsmallpage\t%d' % self.regex_list
            else:
                return u'\t%s\t' % self.method + self.match_str()

        def _create_regex_list(self):
            ent_list = self.regex_list_str.split(u'\t')
            ret = list()
            in_not = in_and = False
            for ent in ent_list:
                if ent == 'not':
                    if in_not:
                        raise ConfError(self.regex_list_str)
                    ret.append(False)
                    in_not = True
                elif ent == 'and':
                    if in_and or in_not:
                        raise ConfError(self.regex_list_str)
                    in_and = True
                else:
                    if len(ret) > 0 and not in_and and not in_not:
                        raise ConfError(self.regex_list_str)
                    ret.append(re.compile(ent))
                    in_and = in_not = False
            if in_not or in_and:
                raise ConfError(self.regex_list_str)
            return ret

    class AsynRule(object):
        def __init__(self, url_format, params, http_method=u"get"):
            self.url_format = url_format
            self.params_str = params
            self.params_dict = self._create_params_dict()
            self.http_method = http_method

        def __str__(self):
            str_list = list()
            str_list.append(u'\tasyn(%s)\t%s' % (self.http_method[0].upper(), self.url_format))
            for k, v in self.params_dict.iteritems():
                str_list.append(u'%s(%s)=%s' % (k, v[0], v[1].pattern))
            return u'\t'.join(str_list)

        def _create_params_dict(self):
            ret = dict()
            params_list = self.params_str.split(u'\t')
            if len(params_list) == 0:
                raise ConfError('asyn\t%s\t%s' % (self.url_format, self.params_str))
            for param in params_list:
                ent = param.split(u'=', 1)
                if len(ent) != 2:
                    raise ConfError('asyn\t%s\t%s' % (self.url_format, self.params_str))
                m = re.match(re.compile(ur'([0-9A-Za-z_]+)(\((.)\))?$'), ent[0].strip())
                if m is None or (m.group(3) and m.group(3) != u'p' and m.group(3) != u'u'):
                    raise ConfError('asyn\t%s\t%s' % (self.url_format, self.params_str))
                vid_pat = re.compile(ent[1])
                if len(vid_pat.groupindex) != 1:
                    raise ConfError('please give a symbolic group name to patten, like: (?P<name>...): ' +
                                    '[asyn\t%s\t%s]' % (self.url_format, self.params_str))
                if m.group(3): value_from = m.group(3)
                else: value_from = u'p'
                ret[m.group(1)] = (value_from, vid_pat)
            if len(ret) == 0:
                raise ConfError('asyn\t%s\t%s' % (self.url_format, self.params_str))
            return ret

        def generate_params_dict(self, url, page):
            ret = dict()
            for param_name, from_and_re in self.params_dict.iteritems():
                if from_and_re[0] == u'u':
                    m = re.search(from_and_re[1], url)
                else:
                    m = re.search(from_and_re[1], page)
                if m:
                    for _, v in from_and_re[1].groupindex.iteritems():
                        ret[param_name] = m.group(v)
            logging.info('async params: %s' % ret)
            if len(ret) != len(self.params_dict):
                return None
            return ret


class AsynConf(object):
    def __init__(self, page_regex_str, methods_str):
        self.page_regex_str = page_regex_str
        self.page_regex = re.compile(self.page_regex_str)
        if not methods_str or methods_str == u"*":
            methods_str = u'body'
        self.method = tuple(methods_str.split(ur'|'))
        self.rules = list()

    def __str__(self):
        site_str_list = list()
        site_str_list.append(u'asyn_regex\t%s\t%s' % (self.page_regex_str, u'|'.join(self.method)))
        map(lambda x: site_str_list.append(unicode(x)), self.rules)
        return u'\n'.join(site_str_list)


class Conf:
    def __init__(self, conf_dir, page_conf=None, asyn_conf=None):
        self.site_tree = dict()
        self._site_tree_tmp = None
        self.asyn_temp = list()

        self._conf_dir = conf_dir
        self._page_conf = self._conf_dir + os.sep + page_conf
        if not self._page_conf:
            self._page_conf = self._conf_dir + os.sep + 'page_judge.conf'
        self._page_conf_f = None

        self._asyn_conf = self._conf_dir + os.sep + asyn_conf
        if not self._asyn_conf:
            self._asyn_conf = self._conf_dir + os.sep + 'asyn_judge.conf'
        self._asyn_conf_f = None

        self._load_all_conf()
        self._page_conf_mtime = os.stat(self._page_conf).st_mtime
        self._asyn_conf_mtime = os.stat(self._asyn_conf).st_mtime

    def __str__(self):
        conf_str_list = list()
        conf_str_list.append('[page_judge.conf: %s]' %
                             (datetime.fromtimestamp(self._page_conf_mtime).strftime('%Y-%m-%d %H:%M:%S')))
        site_conf_list = list()
        self._all_node(site_conf_list, self.site_tree)
        map(lambda x: conf_str_list.append(unicode(x)), site_conf_list)
        conf_str_list.append('[asyn_judge.conf: %s]' %
                             (datetime.fromtimestamp(self._asyn_conf_mtime).strftime('%Y-%m-%d %H:%M:%S')))
        map(lambda x: conf_str_list.append(unicode(x)), self.asyn_temp)
        return u'\n'.join(conf_str_list)

    def _all_node(self, result_list, root):
        if len(root) == 0:
            return
        rule = root.get(u'__conf__')
        if rule is not None:
            result_list.append(rule)
        for k, v in root.iteritems():
            if k == u'__conf__' or k == u'__site__':
                continue
            self._all_node(result_list, v)

    def add_to_site_tree(self, site, methods_str):
        pos_node = self.site_tree
        if site != u'*':
            ent = unicode(site).split('.')
            for node in ent[-1::-1]:
                pos_node = pos_node.setdefault(node, dict())
        pos_node[u'__site__'] = site
        if pos_node.get(u'__conf__', None) is not None:
            raise ConfError('[%s] config already exist' % site)
        site_conf = pos_node.setdefault(u'__conf__', SiteConf(site, methods_str))
        return site_conf

    def get_site_conf(self, url):
        url_ent = urlparse.urlparse(url)
        if len(url_ent[1]) == 0:
            logging.warning('[url:%s] format error' % url)
            return None
        colon_idx = url_ent[1].find(u':')
        if colon_idx != -1:
            site = url_ent[1][0:colon_idx]
        else:
            site = url_ent[1]
        ent = unicode(site).split('.')
        pos_node = self.site_tree
        node_list = list()
        for node in ent[-1::-1]:
            pos_node = pos_node.get(node)
            if pos_node is None or len(pos_node) == 0:
                break
            site_conf = pos_node.get(u'__conf__')
            if site_conf is not None and pos_node.get(u'__site__') is not None:
                if site_conf.page_regex is None or (site_conf.page_regex.match(url)):
                    node_list.append(site_conf)
        if len(node_list) > 0:
            return node_list[-1]
        else:
            return self.site_tree.get(u'__conf__', None)

    def _load_all_conf(self):
        self._page_conf_f = codecs.open(self._page_conf, encoding='gbk')
        self._asyn_conf_f = codecs.open(self._asyn_conf, encoding='gbk')
        self._parse_page_conf()
        self._parse_asyn_conf()
        self._page_conf_f.close()
        self._asyn_conf_f.close()

    def reload_conf_by_mtime(self):
        page_t = os.stat(self._page_conf).st_mtime
        asyn_t = os.stat(self._asyn_conf).st_mtime
        if page_t > self._page_conf_mtime or asyn_t > self._asyn_conf_mtime:
            self.reload_conf()
            self._page_conf_mtime = page_t
            self._asyn_conf_mtime = asyn_t

    def reload_conf(self):
        self._site_tree_tmp = self.site_tree
        self.site_tree = dict()
        try:
            logging.info('CONF: reload config')
            self._load_all_conf()
        except Exception:
            self.site_tree = self._site_tree_tmp
            self._site_tree_tmp = None
            logging.error("parse conf file ERROR")
            logging.error('use the old config')
            return
        logging.info('reload conf success')

    @staticmethod
    def _read_a_line(f):
        while True:
            line = f.readline()
            if not line:
                return None
            logging.debug('[%s]', line[:-1])
            line = line.rstrip()
            line_no_space = line.strip()
            if not line_no_space or line_no_space[0] == u'#':
                continue
            return line

    def _parse_page_conf(self):
        cur_site = None
        while True:
            line = self._read_a_line(self._page_conf_f)
            if not line:
                break
            if line[0] != '\t':
                if line[0:4] != u'site':
                    raise ConfError(line)
                ent = line.split(u'\t')
                if len(ent) != 2 and len(ent) != 3:
                    raise ConfError(line)
                if len(ent) == 2:
                    cur_site = self.add_to_site_tree(ent[1].strip(), None)
                else:
                    cur_site = self.add_to_site_tree(ent[1].strip(), ent[2].strip())
                continue
            if line[1:11] == u'page_regex':
                cur_site.set_page_regex(line[12:])
                continue
            if line[1:5] == u'link' or line[1:5] == u'body' or line[1:5] == u'http':
                cur_site.rules.append(SiteConf.Rule(line[1:5], line[6:]))
                continue
            if line[1:6] == u'title':
                cur_site.rules.append(SiteConf.Rule(line[1:6], line[7:]))
                continue
            if line[1:5] == u'asyn':
                ent = line[1:].split(u'\t', 2)
                if len(ent) != 3:
                    raise ConfError(line)
                if ent[0] == u'asyn' or ent[0] == u'asyn(G)':
                    cur_site.rules.append(SiteConf.AsynRule(ent[1], ent[2], u'get'))
                elif ent[0] == u'asyn[H]':
                    cur_site.rules.append(SiteConf.AsynRule(ent[1], ent[2], u'head'))
                else:
                    raise ConfError(line)
            else:
                raise ConfError(line)

    def _parse_asyn_conf(self):
        cur_conf = None
        while True:
            line = self._read_a_line(self._asyn_conf_f)
            if not line:
                break
            if line[0] != '\t':
                if line[0:10] != u'asyn_regex':
                    raise ConfError(line)
                ent = line.split(u'\t')
                if len(ent) != 2 and len(ent) != 3:
                    raise ConfError(line)
                if len(ent) == 2:
                    cur_conf = AsynConf(ent[1].strip(), None)
                else:
                    cur_conf = AsynConf(ent[1].strip(), ent[2].strip())
                self.asyn_temp.append(cur_conf)
                continue
            if line[1:5] == u'link' or line[1:5] == u'body' or line[1:5] == u'http':
                cur_conf.rules.append(SiteConf.Rule(line[1:5], line[6:]))
                continue
            if line[1:6] == u'title':
                cur_conf.rules.append(SiteConf.Rule(line[1:6], line[7:]))
                continue
            if line[1:5] == u'asyn':
                ent = line[1:].split(u'\t', 2)
                if len(ent) != 3:
                    raise ConfError(line)
                if ent[0] == u'asyn' or ent[0] == u'asyn(G)':
                    cur_conf.rules.append(SiteConf.AsynRule(ent[1], ent[2], u'get'))
                elif ent[0] == u'asyn(H)':
                    cur_conf.rules.append(SiteConf.AsynRule(ent[1], ent[2], u'head'))
                else:
                    raise ConfError(line)
            else:
                raise ConfError(line)


if __name__ == '__main__':
    import logging
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    logging.debug(os.getcwd())
    # current_py_path = os.path.split(os.path.realpath(__file__))[0]
    # conf = Conf(current_py_path + '%s..%s..%sconf' % (os.sep, os.sep, os.sep))
    conf = Conf('conf', 'page_judge.conf', 'asyn_judge.conf')
    # print(unicode(conf))
    logging.info(conf)
    logging.info('============================================')
    site_conf = conf.get_site_conf('http://www.iqiyi.com.cn/v_19rrof35qg.html')
    logging.info(site_conf)
    for r in site_conf.rules:
        logging.info(r)
        if isinstance(r, SiteConf.Rule):
            logging.info(r.check_match(u'BBBBhello world'))
