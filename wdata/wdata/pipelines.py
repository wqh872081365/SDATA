# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2


class WdataPipeline(object):
    def process_item(self, item, spider):
        return item


class PostgresPipeline(object):

    def __init__(self):
        self.connection = psycopg2.connect(host="localhost", database="sdata", user="postgres")
        self.cursor = self.connection.cursor()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        return item