# -*- coding: utf-8 -*-


import json
import sys

import scrapy
from scrapy import Selector

from scrapy_learn4.items import Article
from scrapy_learn4.utils import emailUtil


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    keyword = 'vivo+x20'
    runFlag = True
    baseUrl = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0&sort_by=default"

    authorization = "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
    headers = {"authorization": authorization}

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')

    def start_requests(self):

        # url = "https://www.zhihu.com/r/search?q=vivo+x20&correction=1&type=content&offset=0"
        url = "https://www.zhihu.com/r/search?q={}&correction=1&type=content&offset=0".format(self.keyword)
        yield scrapy.Request(url=url)

    def parse(self, response):
        htmls = json.loads(response.text)['htmls']
        time = 0
        for item in htmls:
            # if time > 4:
            #     break
            # with open('temp.html', 'w') as f:
            #     f.write(item)
            html = Selector(text=item)
            title = html.xpath(".//div[@class='title']").xpath("string()").extract_first()
            author = html.xpath(".//a[@class='author']/text()").extract_first()
            url = html.xpath(".//div[@class='title']/a/@href").extract_first()
            vote_up = html.xpath(".//button[@class='up']/span[@class='count']/text()").extract_first()

            comment_count = html.xpath(".//a[@class='action-item js-toggleCommentBox']/span/text()").extract_first()

            zhunlan_com_id = html.xpath(".//div[@class='content']/meta[@itemprop='post-id']/@content").extract_first()

            print 'zhunlan_com_id:', zhunlan_com_id
            if comment_count:
                comment_count = comment_count.strip().split(" ")[0]
            else:

                comment_count = 0
                print "error is comment_count"
                print "title", title

            if not vote_up:
                vote_up = html.xpath(
                    ".//div[@class='zm-item-vote-count js-expand js-vote-count']/text()").extract_first()

            id = url.split("/")[-1]
            if not url.startswith('http'):

                url = self.baseUrl.format(id)
                yield scrapy.Request(url=url, headers=self.headers, meta={"id": id, 'title': title, "vote_up": vote_up,
                                                                          "comment_count": comment_count, 'url': 'url'},
                                     callback=self.parseNotZhuanlan)
                isZhuanlan = False
            else:
                with open('search.html', 'w') as f:
                    f.write(item)
                isZhuanlan = True
                answers_count = 0
                yield Article(title=title, author=author, id=id, vote_up=vote_up, isZhuanlan=isZhuanlan,
                              comment_count=comment_count, answers_count=answers_count, zhunlan_com_id=zhunlan_com_id)

            time += 1

        nextUrl = json.loads(response.text)['paging']['next']
        if nextUrl:
            url = "https://www.zhihu.com" + nextUrl
            print url
            yield scrapy.Request(url=url)
        else:
            print "over"
        pass

    def parseNotZhuanlan(self, response):
        "解析针对非专栏的提问的作者，和回复数（answers）"
        isZhuanlan = False
        title = response.meta['title']
        data = json.loads(response.text)['data']
        if not data:
            print "data is null:", title
            return

        paging = json.loads(response.text)['paging']
        item = data[0]

        answers_count = paging['totals']
        author = item['question']['author']['name']

        vote_up = response.meta['vote_up']
        id = response.meta['id']
        comment_count = response.meta['comment_count']

        yield Article(title=title, author=author, id=id, vote_up=vote_up, isZhuanlan=isZhuanlan,
                      comment_count=comment_count, answers_count=answers_count, zhunlan_com_id=0)
        pass

    def close(self, reason):  # 爬取结束的时候发送邮件

        with open("exceptions.txt", 'r') as f:
            message = f.read().decode('utf-8')
            emailUtil.sendMsg_QQ(info=(u'具体信息：' + message))
        pass
