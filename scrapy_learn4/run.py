# -*- coding: utf-8 -*-
# @Time : 2017/1/1 17:51
import os

from scrapy import cmdline

# name = 'zhihu'
name = 'test1'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
print 'yuan'
