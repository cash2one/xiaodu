# -*- coding: utf-8 -*-

import sys,os
#from check import CheckData

#from pyspider.libs.check import CheckData
from check import CheckData
check_data=CheckData()

dict = {
    'title': 'abcc' ,
     'link': 'https://v.baidu.com/' ,
     #'link': 'http://baike.baidu.com/link?url=I2LEkE26PXrtXohzZ9j7CMuENmNd30nSFJvwGLEogbkBJbIcbe94fg21CIQPLZPy_vh6Cgb_tL4AX9eceQguYSHITXiiTC7Lxc0bcrPMBSQi-09Of3shKrTBbLg75few' ,
    'horizontal_thumnail_url': 'http://i0.hdslb.com/bfs/archive/281d667ab966a395d3de05be454dbb53dd738225.jpg_320x200.jpg',
    'description':'今天是dfafda     \t\r个好日子啊\n\n',
    'author':'name',
     #'state' : 1, 
    'block':'旅行', 
     #'pub_time':1476762349000,
     #'pub_time':0,
    'pub_time':'2016-8-05',
     #'pub_time':'201109',
    'site':'test',
    'play_count': 1,
    'comment_count':'1.2亿',
    'lalallala':'aaa',
    'hd': None,
    'duration':'72:12',
}


class Handler(object):
    def test(self):
        #dict={}
        #print check.check(dict)
        result=check_data.check(dict)
        if result['num']==0:
            print result['dict']
        else:
            print result['error']
            print result['dict'] 

handler=Handler()
handler.test()
