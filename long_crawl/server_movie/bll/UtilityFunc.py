#-*-coding:utf-8-*-
'''
Created on 2014-7-18
@author: wsx
'''
import subprocess
import re
import sys
import traceback
from utils.LogUtil import Logger

class Funclib(object):
    __logger = Logger.get_logger()
    @staticmethod
    def calc_url_sign(url):
        try:
            cmd = './bin/print_sign %s' % (url)
            obj = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            sign1, sign2 = obj.stdout.read().strip('\n').split('\t')
            return int(sign1), int(sign2)
        except Exception, e:
            t, v, tb = sys.exc_info()
            Funclib.__logger.warning('SIGN FAILED: calc_url_sign() failed, url=%s, errmsg=%s,%s,%s,%s' % (url, e, t, v, traceback.format_tb(tb)))
            return -1, -1
    
    @staticmethod
    def normalize_link_format(work_type, old_link):
        if 'vod.kankan.com' in old_link and '&amp;quality=' in old_link:
            old_link = re.sub('&amp;quality=\d+', '', old_link)
        new_link = old_link
        if 'vod.kankan.com' in old_link and 'subid=' in old_link:
            fields = old_link.split('.shtml?subid=')
            new_link = '%s/%s.shtml?id=731009' % (fields[0], fields[1])
        elif 'www.iqiyi.com' in old_link and 'src=frbdaldjunest' not in old_link:
            new_link = '%s?src=frbdaldjunest' % (old_link)
        elif 'www.wasu.cn' in old_link and 'refer=video.baidu.com' not in old_link:
            new_link = '%s?refer=video.baidu.com' % (old_link)
        elif 'sohu.com' in old_link and 'txid=' not in old_link:
            if 'tv' == work_type:
                new_link =  '%s?txid=10ad708cb3c0cfcd5ea81608c0a558de' % (old_link)
            elif 'variety' == work_type:
                new_link =  '%s?txid=a10088b7031b0ef99d51cd8bb1b92ca5' % (old_link)
            elif 'comic' == work_type:
                new_link =  '%s?txid=29160bffec9cdd135700add26681570f' % (old_link)
        elif 'qq.com' in old_link:
            if 'movie' == work_type:
                new_link = re.sub('(?<=html).+','?ptag=baidu.video.movie', old_link)
        return new_link

    @staticmethod
    def normalize_url(url):
        index = url.find('?')
        if index != -1:
            new_url = url[:index].strip()
            return new_url
        return url.strip()
