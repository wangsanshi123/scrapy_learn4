# -*- coding: utf-8 -*-
import scrapy


class ZhihureplySpider(scrapy.Spider):
    name = "zhihureply"
    start_urls = ['http://ytx.com/']

    authorization = "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
    headers = {"authorization": authorization}
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": headers
    }

    def parse(self, response):
        pass
