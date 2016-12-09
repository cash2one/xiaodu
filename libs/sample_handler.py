#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on __DATE__
# Project: __PROJECT_NAME__
# Authors:
"""
Brief: 

"""

from pyspider.libs.base_handler import *
from pyspider.libs import mimod
import logging
logger = logging.getLogger('cherry')
from pyspider.libs.check import CheckData
from pyspider.libs.dc.dc import dead_detect
check_data = CheckData()

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('__START_URL__', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        res_dict = response.save #your dict
        if dead_detect(res_dict['link']) == 0:
            print  'live_link'
            result = check_data.check(res_dict)
            if result['num']==0:
                try:
                    logger.info('send to mimod: %s', str(result['dict']))
                    ret, code, resp = mimod.send_to_mimod(result['dict'])
                    #print ret, code, resp
                    return result['dict']
                except Exception as ee:
                    print ee
                else:
                    print result['error'] 
        else:
            print  'dead_link'

