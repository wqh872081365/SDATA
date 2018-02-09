# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from app.video.models import BilibiliSeason
from app.proxy.models import Proxy
from app.logs.models import SpiderLog


class WdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BilibiliSeasonItem(DjangoItem):
    django_model = BilibiliSeason

    complete = scrapy.Field()


class ProxyItem(DjangoItem):
    django_model = Proxy


class SpiderLogItem(DjangoItem):
    django_model = SpiderLog
