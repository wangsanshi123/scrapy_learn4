# -*- coding: utf-8 -*-


import json
import sys

import scrapy
from scrapy import Selector

from scrapy_learn4.items import Article
from scrapy_learn4.utils import emailUtil


class ZhihuSpider(scrapy.Spider):
    name = "360library"

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')

    def start_requests(self):
        url = "http://www.360doc.com/content/16/1202/12/38579529_611275213.shtml"
        url = "http://www.360doc.com/content/15/1013/08/25285926_505261931.shtml"
        yield scrapy.Request(url=url)

    def parse(self, response):
        content = response.xpath(".//*[@id='artContent']/div")
        print len(content)
        for item in content:
            item = item.xpath("string()").extract_first()
            if item:
                text = item + "\n"
                with open("360library2.txt", "a")as f:
                    f.write(text)
            else:
                print "item is  null"
        pass

    def close(self, reason):  # 爬取结束的时候发送邮件

        with open("exceptions.txt", 'r') as f:
            message = f.read().decode('utf-8')
            emailUtil.sendMsg_QQ(info=(u'具体信息：' + message))
        pass
