#!/usr/bin/env python
#coding:utf8
import random,threading,time
import httplib, urllib
import json
from Queue import Queue
import pdb
import sys
import BeautifulSoup

def insert_data(table, insert_value):
    if len(insert_value) <= 0:
        return ""

    insert_col=''
    insert_val=''
    for key, value in insert_value.items():
        if insert_col == '':
            insert_col = key
            insert_val = "'" + str(escape_mysql_str(value)) + "'"
        else:
            if key == 'insert_time':
                insert_col = insert_col + " , " + key
                insert_val = insert_val + " , " + str(escape_mysql_str(value)) + ""
            else:
                insert_col = insert_col + " , " + key
                insert_val = insert_val + " , '" + str(escape_mysql_str(value)) + "'"
    res = "insert ignore into " + table + "(" + insert_col + " ) values (" + insert_val + ");\n"
    return res
def escape_mysql_str(str):
    ct = str
    if "'" in ct:
        ct = ct.replace("'","\\'")
    if "\"" in ct:
        ct = ct.replace("\"","\\\"")
    return ct

def parse_one_record(sec):
    try:
        data_json = {}
        data_json['pub_time'] = str(sec['hot-time'])
        data_json['title'] = sec.a.h3.text.encode('utf-8','ignore')
        data_json['link'] = 'http://www.toutiao.com%s' % (sec.a['href'])
        data_json['thumnail_url'] = sec.a.contents[3].img['src']
        data_json['app_name'] = u'toutiao'
        data_json['state'] = u'1'
        data_json['insert_time'] = u'current_timestamp'
        data_json['author'] = sec.a.contents[1].contents[3].contents[1].text.encode('utf-8','ignore')
        pinglun_str = sec.a.contents[1].contents[3].contents[3].text.encode('utf-8','ignore')
        data_json['comment_count'] = pinglun_str[pinglun_str.find(';') + 1:]
#check ad 
        if '_as_' in data_json['link'] or 'large' in data_json['thumnail_url']:
            return
        if 'ad-label' in sec:
            return
#change
        data_json['thumnail_url'] = data_json['thumnail_url'].replace("list", "large")
        print insert_data("crawl_data",data_json)
#        print sec.a.contents[1].contents[3].contents[1].text.encode('utf-8','ignore')
#        print sec.a.contents[1].contents[3].contents[3].text.encode('utf-8','ignore')
    except Exception, e:
        sys.stderr.write('parse_one_record exception:%s' %(str(e)))
    
def parse_html(html_ct):
    try:
        soup = BeautifulSoup.BeautifulSoup(html_ct)
        for i in range(0,len(soup.contents)):
            if len(str(soup.contents[i])) <= 10 :
                continue
            sec1 = soup.contents[i]
            parse_one_record(sec1)
    except Exception, e:
        sys.stderr.write('parse_html exception:%s' %(str(e)))
    


headers = {"Accept": "*/*", \
        "Pragma":"no-cache", "Host":"m.toutiao.com", \
        "User-Agent":"curl/7.12.1 (x86_64-redhat-linux-gnu) libcurl/7.12.1 OpenSSL/0.9.7a zlib/1.2.1.2 libidn/0.5.6"}
params = ""
uri = "/list/?tag=video&ac=wap&item_type=4&count=20&format=json&list_data_v2=1&ad_pos=4&ad_gap=6&as=A115D74E483FC4E&cp=57E81FFC64FE7E1&csrfmiddlewaretoken=6607c4b5282c4d2b79689b792f570813&max_behot_time=%d" % (int(time.time()))
conn = httplib.HTTPConnection("m.toutiao.com")
conn.request("GET",uri, params, headers)
response = conn.getresponse()
ret_json = json.loads(response.read())
conn.close()
if response.status == 200 and 'html' in ret_json:
    html_ct = ret_json['html'].encode('utf-8','ignore')
    parse_html(html_ct)
