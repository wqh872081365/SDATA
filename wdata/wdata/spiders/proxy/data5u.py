# -*- coding: utf-8 -*-

import scrapy


class data5uSpider(scrapy.Spider):
    name = "data5u"

    def start_requests(self):
        urls = [
            "http://www.data5u.com/free/index.shtml",
            "http://www.data5u.com/free/gngn/index.shtml",
            "http://www.data5u.com/free/gnpt/index.shtml",
            "http://www.data5u.com/free/gwgn/index.shtml",
            "http://www.data5u.com/free/gwpt/index.shtml"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass