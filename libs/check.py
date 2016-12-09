# -*- coding: utf-8 -*-
"""
Brief: 健康检查
Authors: Ma ZeYi
Date: 2016-10-17 15:46:00
"""
import os
import sys
import time
import re
from dc.dc import dead_detect
from datetime import datetime
reload(sys) 
sys.setdefaultencoding('utf-8')



class CheckData(object):

    def __init__(self):     
        self.columns_must = set(('title', 'block', 'site', 'link'))
        self.columns_int = set(('play_count','up_count','down_count','comment_count','pub_time','duration','hd'))
        self.columns_str = set(('description', 'author', 'horizontal_thumnail_url', 'vertical_thumnail_url', 'real_link'))
        self.blocks = set(('热门','体育','游戏','资讯','音乐','搞笑','生活','动漫','娱乐','美食','旅行','科技','亲子','汽车','财经','时尚','原创','教育','公益','拍客','舞蹈','美女','少儿','电影'))
         
        self.columns=set()
        self.columns.update(self.columns_must)
        self.columns.update(self.columns_int)
        self.columns.update(self.columns_str)
        
        self.http_columns = set(('horizontal_thumnail_url','vertical_thumnail_url','link','real_link'))
        self.site='no_site'
        self.block='no_block'
        self.result = {
            'num':0 ,
            'error':'' ,
            'dict' : {}
        }

    def cur_file_dir(self):
        path = sys.path[0]
        if os.path.isdir(path):
            return str(path)
        elif os.path.isfile(path):
            return str(os.path.dirname(path))

    def log(self,message):
        timestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logstr = '%s %s %s: %s\n' % (timestr,self.site,self.block, message)
        self.result['error']=self.result['error']+logstr                   
        self.result['num']+=1
        #filename=self.cur_file_dir()+'/../log/'+self.site+'.log'
        filename='/home/video/dist_pyspider/log/'+self.site+'.log'
        file_object = open(filename, 'a+')
        file_object.write(logstr)
        file_object.close()
   
    #检查block
    def check_block(self,dict):
        if "block" in dict.keys():
            self.block=dict['block']
            block=str(dict['block']).encode('utf8')
            if block not in self.blocks:
                self.log('block error: '+dict['block'])

 
    #合并字典 
    def merge_dict(self,to, from_, callback=None, exclude=None, include=None):
        def _check_key(k, inc, exc):
            if inc:
                return k in inc
            elif exc:
                return k not in exc
            return True
        if not callback:
            callback = lambda k, v, to: True
        for k, v in from_.items():
            if _check_key(k, inc=include, exc=exclude) and callback(k, v, to):
                if v == None:
                    continue
                else:
                    to[k] = v
            else:
                self.log('key error: '+k)
        return to

    #字符转化为数字
    def trans_to_int(self,v):
        if v=='':
            return 0
        try:
            #v=str(v)
            #if "\xe4\xb8\x87" in v:
            #    v=v.replace('\xe4\xb8\x87','')
            #    v=int(v)*10000
            v=str(v).encode('utf-8') 
            if "亿" in v:
                v=v.replace('亿','')
                v=int(float(v)*100000000)
            elif "万" in v:
                v=v.replace('万','')
                v=int(float(v)*10000)
            elif "千" in v:
                v=v.replace('千','')
                v=int(float(v)*1000)
            else:
                v=int(v)
        except Exception as e:
            self.log("exception: "+str(e))
            v=0
        finally:
            return v

    #pubtime时间格式化
    def time_rush(self,t):
        try:
            if '-' in str(t):
                if len(str(t))<11:
                    t=time.mktime(time.strptime(t,'%Y-%m-%d'))
                else:
                    t=time.mktime(time.strptime(t,'%Y-%m-%d %H:%M:%S'))
            t=int(t)
            if len(str(t))>10:
                t=int(str(t)[:10])
            elif len(str(t))<10:
                self.log('exception: pub_time : '+str(t))
                t=int(time.time())
        except Exception as e:
            self.log('exception: pub_time : '+str(t)+', '+str(e)) 
            t=int(time.time()) 
        finally:
            return t
    
    #正文描述清洗
    def text_rush(self,text):
        text=text.replace('<br>', '').replace('<br/>', '').replace('\r', '').replace('\n', '')
        text=re.sub('[\t\r ]+', ' ', text)
        return text    
    
    #时长转换   
    def duration_rush(self,s):
        time=0
        try:
            if ":" in str(s):
                list=str(s).split(':')
                if len(list)==3:
                    time=int(list[0])*3600+int(list[1])*60+int(list[2])
                elif len(list)==2:
                    time=int(list[0])*60+int(list[1])
                else:
                    self.log('duration error: '+str(s))
            else:
                time=int(float(s))
        except Exception as e:
            self.log('exception: duration : '+str(s)+', '+str(e))
        finally:
            return time
    
    #hd转换
    def hd_rush(self,s):
        hd=0
        try:
            if "标清" in str(s):
                hd=1
            elif "高清" in str(s):
                hd=2
            elif "超清" in str(s):
                hd=3
            elif "720" in str(s):
                hd=2
            elif "1080" in str(s):
                hd=3
            else:
                hd=int(s)
                if hd>3 or hd<0:
                    self.log('exception: hd : '+str(hd))
                    hd=0 
        except Exception as e:
            self.log('exception: hd : '+str(s)+', '+str(e))
        finally:
            return hd
     
         

    #必须字段检查
    def check_must_key(self,dict):
        for column in self.columns_must:
            if column in dict.keys(): 
                if dict[column]=='':
                    self.log('empty value: '+str(column))
            else:
                self.log('no key: '+str(column))
        
        if 'horizontal_thumnail_url' not in dict.keys() and 'vertical_thumnail_url' not in dict.keys():
            self.log('no key: horizontal_thumnail_url/vertical_thumnail_url')



    #url检查&死链检测
    def check_http_key(self,dict):
        for column in self.http_columns:
            if column in dict.keys():
                if dict[column]=='':
                    continue
                elif "http" not in dict[column]:
                    self.log('url error: '+column+': '+dict[column])
                elif column =='link': 
                    try:
                        if dead_detect(dict[column]) != 0:
                            self.log('dead link: '+dict[column])
                    except Exception as e:
                        self.log('dead link and excepiton: '+dict[column])

    #清洗字段
    def rush_key(self,dict):
        may_value = {
            #'state' : 1,
            'description' : '',
            'horizontal_thumnail_url':'',
            'vertical_thumnail_url':'',
            'author' : '',
            'real_link' :'',
            'pub_time' : int(time.time()),
            #'insert_time' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'play_count' : 0,
            'up_count' : 0,
            'down_count' : 0,
            'comment_count' : 0,
            'duration': 0,
            'hd': 0,
        }

        try:   
            #排除多余字段,补充未填字段
            dict=self.merge_dict(may_value,dict,include=self.columns)
            #字段清洗
            dict['pub_time']=self.time_rush(dict['pub_time'])
            dict['description']=self.text_rush(dict['description'])
            dict['title']=self.text_rush(dict['title'])
            dict['duration']=self.duration_rush(dict['duration'])
            dict['hd']=self.hd_rush(dict['hd'])
            ##str转int
            for column in self.columns_int:
                dict[column]=self.trans_to_int(dict[column]) 
        except Exception as e:
            self.log('exception:'+str(e))
        finally:
            return dict

        
    #开启健康检查
    def check(self,dict):
        if dict is None:
            self.log('dict is None')
            return self.result
        if "site" in dict.keys():
            self.site=dict['site']        
            
        self.check_block(dict)
        self.check_must_key(dict)
        self.check_http_key(dict)
        dict=self.rush_key(dict)
        self.result['dict']=dict
        return self.result


