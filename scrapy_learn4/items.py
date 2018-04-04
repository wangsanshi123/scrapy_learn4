# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyLearn4Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JubiItem(scrapy.Item):
    date = scrapy.Field()

    token = scrapy.Field()
    open = scrapy.Field()
    max = scrapy.Field()
    close = scrapy.Field()
    min = scrapy.Field()
    amount = scrapy.Field()


class Article(scrapy.Item):

    title = scrapy.Field()
    comment_count = scrapy.Field()
    isZhuanlan = scrapy.Field()
    author = scrapy.Field()
    vote_up = scrapy.Field()
    id = scrapy.Field()
    answers_count = scrapy.Field()
    zhunlan_com_id = scrapy.Field()

class Comments(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()


    createdTime = scrapy.Field()
    isOrg = scrapy.Field()

    gender = scrapy.Field()
    user_type = scrapy.Field()
    type = scrapy.Field()
    is_advertiser = scrapy.Field()
    vote_count = scrapy.Field()
    isZhuanlan = scrapy.Field()
    comment_id = scrapy.Field()

