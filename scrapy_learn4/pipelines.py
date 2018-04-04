# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

from scrapy_learn4.items import JubiItem, Article, Comments

logger = logging.getLogger(__name__)


class MySQLStoreCnblogsPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        self.i = 0

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        if isinstance(item, JubiItem):
            d = self.dbpool.runInteraction(self._process_jubi, item, spider)
        if isinstance(item, Article):
            d = self.dbpool.runInteraction(self._process_zhihu_article, item, spider)
        if isinstance(item, Comments):
            d = self.dbpool.runInteraction(self._process_zhihu_comments, item, spider)



        else:
            d = self.dbpool.runInteraction(self._process_nothing, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    # 将每行更新或写入数据库中
    def _process_jubi(self, conn, item, spider):
        try:
            conn.execute("insert into jubi VALUES (%s,%s,%s,%s,%s,%s,%s)",
                         (item['date'], item['token'], item['open'],
                          item['max'], item['close'], item['min'], item['amount']))
        except Exception, e:
            logger.error(e)
            pass

        pass

    def _process_zhihu_article(self, conn, item, spider):
        try:
            conn.execute("insert into zhihu_article VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                         (item['title'], item['comment_count'], item['isZhuanlan'],
                          item['author'], item['vote_up'], item['id'], item['answers_count'], item['zhunlan_com_id']))
        except Exception, e:
            logger.error(e)
            pass

        pass

    def _process_zhihu_comments(self, conn, item, spider):
        try:
            conn.execute("insert into zhihu_comments VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                         (item['id'], item['comment_id'], item['name'], item['content'],
                          item['createdTime'], item['isOrg'], item['gender'], item['user_type'], item['type'],
                          item['is_advertiser'], item['vote_count'], item['isZhuanlan']))
        except Exception, e:
            logger.error(e)
            pass

        pass

    def _process_nothing(self, conn, item, spider):
        # do nothing

        pass
        # 异常处理

    def _handle_error(self, failure, item, spider):
        logging.log.err(failure)
