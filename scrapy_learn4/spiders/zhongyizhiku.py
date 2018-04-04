# -*- coding: utf-8 -*-
import scrapy


class ZhongyizhikuSpider(scrapy.Spider):
    name = "zhongyizhiku"

    def start_requests(self):
        url = "http://baike.zk120.com/wiki/%E6%B1%A4%E5%A4%B4%E6%AD%8C%E8%AF%80_%E7%99%BD%E8%AF%9D%E7%89%88#.E4.BA.8C.E3.80.81.E5.8F.91.E8.A1.A8.E4.B9.8B.E5.89.82"
        yield scrapy.Request(url)

    def parse(self, response):
        ps = response.xpath(".//*[@id='mw-content-text']/p")
        for p in ps:
            result = p.xpath("string()").extract_first()
            if result:
                result += "\n"
                with open("zyzhiku1.txt", "a")as f:
                    f.write(result.encode("utf-8"))
            else:
                print "result is null"
        pass
