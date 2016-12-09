#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/10/26 下午1:52
# @Author  : Sheng Zeng
# @Site    : 
# @File    : 死链测试.py
# @Software: PyCharm
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import socket
socket.setdefaulttimeout(3)
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
#把redirect关闭就可以了。在send时，加上参数allow_redirects=False
#通常每个浏览器都会设置redirect的次数。如果redirect太多会把CPU耗尽。所以redirect几次就会强制中止。
#target_url = 'http://v.youku.com/v_show/id_XMTc2NzMxNTM5Mg==.html'
filename = sys.argv[1]
fw = open('./code_status/'+filename,'a')
sum_count = 0
success_count = 0
success_count1 = 0
for line in open('./sql/'+filename,'r'):
    sum_count += 1
    if sum_count > 800:
        break
    real_link = line.strip().split('\t')[1]
    sign_link = 'http://baidu.'+filename+'/watch/'+line.strip().split('\t')[-1]+'.html?page=videoMultiNeed'
    try:
        r = requests.get(real_link,allow_redirects=False,headers=headers)
        #print r.status_code,r.url,len(r.text),r.headers
        if r.status_code==200 or r.status_code==302:
            success_count += 1
            print 'real_link success:%s' % (real_link)
        else:
            print 'real_link failed:%s\t%d' % (real_link, r.status_code)
    except Exception as ee:
        print ee
        pass
    try:
        r1 = requests.get(sign_link, allow_redirects=False, headers=headers)
        # print r.status_code,r.url,len(r.text),r.headers
	if u'很抱歉，您要访问的页面不存在' in r1.text:
            print 'sign_link failed:%s' % sign_link
        else:
            success_count1 += 1
            print 'sign_link success:%s' % (sign_link)
    except Exception as ee:
        print ee
        pass
    #break

fw.write('%s-%d\n' % (filename,sum_count))
fw.write('%s-real_link\t%d\n' % (filename,success_count))
fw.write('%s-sign_link\t%d\n' % (filename,success_count1))
fw.flush()

