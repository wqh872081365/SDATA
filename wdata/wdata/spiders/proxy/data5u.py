# -*- coding: utf-8 -*-

from django.utils import timezone
from django.conf import settings as sdata_settings
import scrapy
import logging

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


class Data5uSpider(scrapy.Spider):
    name = "data5u"

    def start_requests(self):
        urls = [
            "http://www.data5u.com/free/index.shtml",
            "http://www.data5u.com/free/gngn/index.shtml",
            # "http://www.data5u.com/free/gnpt/index.shtml",
            # "http://www.data5u.com/free/gwgn/index.shtml",
            # "http://www.data5u.com/free/gwpt/index.shtml",

            # anonymity
            "http://www.data5u.com/free/anoy/高匿/index.html",
            # "http://www.data5u.com/free/anoy/%E5%8C%BF%E5%90%8D/index.html",
            # "http://www.data5u.com/free/anoy/%E9%80%8F%E6%98%8E/index.html",

            # http
            "http://www.data5u.com/free/type/http/index.html",
            # "http://www.data5u.com/free/type/socks5/index.html",
            "http://www.data5u.com/free/type/https/index.html",
            # "http://www.data5u.com/free/type/socks4/index.html",

            # country
            "http://www.data5u.com/free/country/中国/index.html",

            # city
            # "http://www.data5u.com/free/area/%E5%8C%97%E4%BA%AC%E5%B8%82/index.html",
            # ......

            # isp
            "http://www.data5u.com/free/isp/电信/index.html",
            "http://www.data5u.com/free/isp/联通/index.html",
            "http://www.data5u.com/free/isp/阿里云/index.html",
            "http://www.data5u.com/free/isp/移动/index.html",
            # ......

        ] + ["http://www.data5u.com/free/area/%s/index.html" % (area,) for area in [
            "广东省", "陕西省", "河南省", "江西省", "广西", "上海市", "安徽省", "河北省", "江苏省", "四川省", "福建省",
            "湖南省", "浙江省", "山东省", "北京市", "湖北省"]]
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
            port = sel.xpath("span[2]/li/@class").extract()
            anonymity = sel.xpath("span[3]/li/a/text()").extract()
            http = sel.xpath("span[4]/li/a/text()").extract()
            country = sel.xpath("span[5]/li/a/text()").extract()
            city = sel.xpath("span[6]/li/a/text()").extract()
            isp = sel.xpath("span[7]/li/a/text()").extract()
            delay = sel.xpath("span[8]/li/text()").extract()
            verify_time = sel.xpath("span[9]/li/text()").extract()

            self.log(str([ip, port, anonymity, http, country, city, isp, delay, verify_time]), logging.INFO)
            print(ip, port, anonymity, http, country, city, isp, delay, verify_time)

            if ip and port:
                try:
                    ip = ip[0].strip()
                    port = int(
                        "".join([str("ABCDEFGHIZ".index(_port)) for _port in port[0].strip().split(" ")[1]])) >> 3
                    anonymity = [_anonymity.strip() for _anonymity in anonymity]
                    country = [_country.strip() for _country in country]
                    http_tem = [_http.strip() for _http in http]
                    http = []
                    for _http in http_tem:
                        if "," in _http:
                            http += [_http_tem.strip() for _http_tem in _http.split(",")]
                        else:
                            http += [_http]
                    for index, _http in enumerate(http):
                        if " " in _http:
                            http[index] = "".join(
                                [_http_sub.strip() for _http_sub in _http.split(" ") if _http_sub.strip()])
                    city = [_city.strip() for _city in city]
                    isp = [_isp.strip() for _isp in isp]
                    delay = [_delay.strip() for _delay in delay]
                    verify_time = [_verify_time.strip() for _verify_time in verify_time]

                    proxy = ProxyItem()
                    proxy["ip"] = ip
                    proxy["port"] = port
                    if anonymity:
                        proxy["anonymity"] = ANONYMITY_DICT.get(anonymity[0], "-1")
                    else:
                        proxy["anonymity"] = "-1"
                    if country:
                        proxy["country"] = country[0]
                    else:
                        proxy["country"] = ""
                    if http:
                        proxy["http"] = "1" if "https" in http else HTTP_DICT.get(http[0], "-1")
                    else:
                        proxy["http"] = "-1"
                    proxy["detail"] = {
                        "anonymity": " ".join(anonymity),
                        "country": " ".join(country),
                        "http": " ".join(http),
                        "city": " ".join(city),
                        "isp": " ".join(isp),
                        "delay": " ".join(delay),
                        "verify_time": " ".join(verify_time),
                        "source": "data5u",
                        "update_time": timezone.localtime(timezone.now()).strftime(sdata_settings.LOG_DATE_FORMAT)
                    }
                    print(proxy)
                    yield proxy
                except Exception as e:
                    print(e)
                    self.log(e, logging.ERROR)
                    continue
