# -*- coding: utf-8 -*-
import json
from time import strptime, strftime

import scrapy
import sys

from scrapy_learn4.items import Comments
from scrapy_learn4.utils.databaseUtil import MysqlUtil
from scrapy_learn4.utils.timeUtil import formatTimestamp


class ZhihureplySpider(scrapy.Spider):
    name = "zhihucomments"
    url = "https://www.zhihu.com/api/v4/questions/29089042/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=10&offset=0&status=open"
    comments_baseUrl = "https://www.zhihu.com/api/v4/questions/{}/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=10&offset=0&status=open"
    comments_zhuanlanUrl = "https://www.zhihu.com/r/posts/{}/comments"
    comments_zhuanlanUrl_sec = "https://www.zhihu.com/r/posts/{}/comments?page={}"
    authorization = "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
    headers = {"authorization": authorization}

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.mysqlUtil = MysqlUtil()

    def start_requests(self):
        self.mysqlUtil.cur.execute('select * from zhihu_article where comments_count>0')
        self.mysqlUtil.conn.commit()
        dataSet = self.mysqlUtil.cur.fetchall()
        time = 0
        for item in dataSet:
            if time > 5:
                break
            id = item['id']
            isZhuanlan = item['isZhuanlan']
            zhuanlan_com_id = item['zhunlan_com_id']
            if isZhuanlan:
                url = self.comments_zhuanlanUrl.format(zhuanlan_com_id)
                yield scrapy.Request(url=url, meta={"isZhuanlan": True, "id": id, "zhuanlan_com_id": zhuanlan_com_id})
                pass
            else:
                url = self.comments_baseUrl.format(id)
                yield scrapy.Request(url=url, headers=self.headers, meta={"id": id})
            time += 1
            pass

    def parse(self, response):
        try:
            isZhuanlan = response.meta['isZhuanlan']
        except:
            isZhuanlan = False
            pass
        paging_ = json.loads(response.text)['paging']

        data = json.loads(response.text)['data']
        id = response.meta["id"]
        zhuanlan_com_id = response.meta["zhuanlan_com_id"]
        if isZhuanlan:
            comment_count = paging_['totalCount']
            perPage = paging_['perPage']
            currentPage = paging_['currentPage']
            print "isZhuanlan"
            for item in data:
                name = item['author']['name']
                content = item['content']
                # content = content.decode('string-escape')
                createdTime = item['createdTime']
                comment_id = item['id']

                str_time = strptime(createdTime.split("+")[0], "%Y-%m-%dT%H:%M:%S")
                createdTime = strftime("%Y-%m-%d %H:%M:%S", str_time)

                try:
                    isOrg = item['author']['isOrg']
                except Exception, e:
                    isOrg = False
                    pass

                print "name:", name, "\n"
                print "content:", content, "\n"
                # print "createdTime:", createdTime, "\n"
                # print "isOrg:", isOrg, "\n"
                yield Comments(id=id, name=name, content=content, createdTime=createdTime, isOrg=isOrg,
                               gender=2, user_type="", type="", is_advertiser=False, vote_count=0, isZhuanlan=True,
                               comment_id=comment_id)
            pass
            if comment_count / perPage + 1 > currentPage:
                yield scrapy.Request(url=self.comments_zhuanlanUrl_sec.format(zhuanlan_com_id, currentPage + 1),
                                     meta={"isZhuanlan": True, "id": id, "zhuanlan_com_id": zhuanlan_com_id})
        else:
            comment_count = paging_['totals']
            next = paging_['next']
            print "is not  Zhuanlan"

            for item in data:
                content = item['content']
                author = item['author']['member']
                gender = author['gender']
                name = author['name']
                user_type = author['user_type']
                type = author['type']
                is_advertiser = author['is_advertiser']
                is_org = author['is_org']
                vote_count = item['vote_count']
                created_time = item['created_time']
                created_time = formatTimestamp(created_time)

                comment_id = item['id']
                # print name, "\n"
                # print created_time, "\n"
                # print is_org, "\n"
                # print content, "\n"
                yield Comments(id=id, name=name, content=content, createdTime=created_time, isOrg=is_org,
                               gender=gender, user_type=user_type, type=type, is_advertiser=is_advertiser,
                               vote_count=vote_count, isZhuanlan=False, comment_id=comment_id)
            is_end = paging_["is_end"]
            if is_end is "false" or "False":
                yield scrapy.Request(url=next, headers=self.headers, meta={"id": id})

        pass
