# -*- coding: utf-8 -*-
import scrapy

from scrapy_learn4.utils import emailUtil


class Test1Spider(scrapy.Spider):
    name = "test1"
    start_urls = ['https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%9B%BD%E5%AE%B6%E5%9C%B0%E7%90%86']

    def parse(self, response):
        print "response"
        pass

    def close(self, reason):  # 爬取结束的时候发送邮件
        print u'close'
        with open("exceptions.txt", 'r') as f:
            message = f.read().decode('utf-8')
            emailUtil.sendMsg_QQ(info=(u'具体信息：' + message))
        pass
