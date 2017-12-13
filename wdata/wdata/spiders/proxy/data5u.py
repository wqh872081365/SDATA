# -*- coding: utf-8 -*-

import scrapy
from wdata.items import ProxyItem

ANONYMITY_DICT = {
    "透明": "0",
    "匿名": "1",
    "高匿": "2"
}

HTTP_DICT = {
    "http": "0",
    "https": "1",
    "socks4": "2",
    "socks5": "3"
}


class data5uSpider(scrapy.Spider):
    name = "data5u"

    def start_requests(self):
        urls = [
            "http://www.data5u.com/free/index.shtml",
            # "http://www.data5u.com/free/gngn/index.shtml",
            # "http://www.data5u.com/free/gnpt/index.shtml",
            # "http://www.data5u.com/free/gwgn/index.shtml",
            # "http://www.data5u.com/free/gwpt/index.shtml",

            # anonymity
            # "http://www.data5u.com/free/anoy/%E9%AB%98%E5%8C%BF/index.html",
            # "http://www.data5u.com/free/anoy/%E5%8C%BF%E5%90%8D/index.html",
            # "http://www.data5u.com/free/anoy/%E9%80%8F%E6%98%8E/index.html",

            # http
            # "http://www.data5u.com/free/type/http/index.html",
            # "http://www.data5u.com/free/type/socks5/index.html",
            # "http://www.data5u.com/free/type/https/index.html",
            # "http://www.data5u.com/free/type/socks4/index.html",

            # country
            # "http://www.data5u.com/free/country/%E4%B8%AD%E5%9B%BD/index.html",

            # city
            # "http://www.data5u.com/free/area/%E5%8C%97%E4%BA%AC%E5%B8%82/index.html",
            # "http://www.data5u.com/free/area/%E4%B8%8A%E6%B5%B7%E5%B8%82/index.html",
            # ......

            # isp
            # "http://www.data5u.com/free/isp/%E7%94%B5%E4%BF%A1/index.html",
            # "http://www.data5u.com/free/isp/%E8%81%94%E9%80%9A/index.html",
            # "http://www.data5u.com/free/isp/%E9%98%BF%E9%87%8C%E4%BA%91/index.html",
            # ......

        ]

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
            "Connection": "keep-alive",
            "Host": "www.data5u.com",
            "Referer": "http://www.data5u.com/",
            "Upgrade-Insecure-Requests": 1,
        }

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        sel_list = response.xpath("//ul[@class='l2']")
        for sel in sel_list:
            ip = sel.xpath("span[1]/li/text()").extract()
            port = sel.xpath("span[2]/li/text()").extract()
            anonymity = sel.xpath("span[3]/li/a/text()").extract()
            http = sel.xpath("span[4]/li/a/text()").extract()
            country = sel.xpath("span[5]/li/a/text()").extract()
            city = sel.xpath("span[6]/li/a/text()").extract()
            isp = sel.xpath("span[7]/li/a/text()").extract()
            delay = sel.xpath("span[8]/li/text()").extract()
            verify_time = sel.xpath("span[9]/li/text()").extract()
            
            print(ip, port, anonymity, http, country, city, isp, delay, verify_time)

            if ip and port:
                try:
                    ip = ip[0].strip()
                    port = int(port[0].strip())
                    anonymity = [anony.strip() for anony in anonymity]
                    country = country[0].strip()
                    http = [ht.strip() for ht in http]
                    city = [ci.strip() for ci in city]
                    isp = isp[0].strip()
                    delay = delay[0].strip()
                    verify_time = verify_time[0].strip()

                    proxy = ProxyItem()
                    proxy["ip"] = ip
                    proxy["port"] = port
                    proxy["anonymity"] = ANONYMITY_DICT.get(anonymity[0], "-1")
                    proxy["country"] = country
                    proxy["http"] = "1" if "https" in http else HTTP_DICT.get(http[0], "-1")
                    proxy["detail"] = {
                        "anonymity": " ".join(anonymity),
                        "http": " ".join(http),
                        "city": " ".join(city),
                        "isp": isp,
                        "delay": delay,
                        "verify_time": verify_time
                    }
                    yield proxy
                except Exception as e:
                    print(e)
                    continue
            break