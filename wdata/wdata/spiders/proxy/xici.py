# -*- coding: utf-8 -*-

from django.utils import timezone

import scrapy
import re

from wdata.items import ProxyItem

ANONYMITY_DICT = {
    "透明": "0",
    "匿名": "1",
    "高匿": "2"
}

HTTP_DICT = {
    "HTTP": "0",
    "HTTPS": "1",
    "socks4": "2",
    "socks5": "3",
    "socks4/5": "-1",
}

COUNTRY_DICT = {
    "Cn": "中国"
}

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Connection": "keep-alive",
    "Host": "www.xicidaili.com",
    "Referer": "http://www.xicidaili.com/",
    "Upgrade-Insecure-Requests": 1,
}


class XiCiSpider(scrapy.Spider):
    name = "xici"

    def start_requests(self):
        urls = [
            "http://www.xicidaili.com/nn/1",
            # "http://www.xicidaili.com/wn/1",
            # "http://www.xicidaili.com/wt/1",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=HEADERS)

    def parse(self, response):
        sel_list = response.xpath("//*[@id='ip_list']//tr")
        for sel in sel_list[1:]:
            country = sel.xpath("td[1]/img/@alt").extract()
            ip = sel.xpath("td[2]/text()").extract()
            port = sel.xpath("td[3]/text()").extract()
            city = sel.xpath("td[4]/a/text()").extract()
            anonymity = sel.xpath("td[5]/text()").extract()
            http = sel.xpath("td[6]/text()").extract()
            delay = sel.xpath("td[8]/div/@title").extract()
            verify_time = sel.xpath("td[10]/text()").extract()

            print(ip, port, anonymity, http, country, city, delay, verify_time)

            if ip and port:
                try:
                    ip = ip[0].strip()
                    port = port[0].strip()
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
                            http[index] = "".join([_http_sub.strip() for _http_sub in _http.split(" ") if _http_sub.strip()])
                    city = [_city.strip() for _city in city]
                    delay = [_delay.strip() for _delay in delay]
                    verify_time = [_verify_time.strip() for _verify_time in verify_time]

                    proxy = ProxyItem()
                    proxy["ip"] = ip
                    proxy["port"] = int(port)
                    if anonymity:
                        proxy["anonymity"] = ANONYMITY_DICT.get(anonymity[0], "-1")
                    else:
                        proxy["anonymity"] = "-1"
                    if country:
                        proxy["country"] = COUNTRY_DICT.get(country[0], "")
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
                        "isp": " ",
                        "delay": " ".join(delay),
                        "verify_time": " ".join(verify_time),
                        "source": "xici",
                        "update_time": timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
                    }
                    print(proxy)
                    yield proxy
                except Exception as e:
                    print(e)
                    continue

        try:
            data, page = re.match(r'^http://www.xicidaili.com/(\w*)/(\d*)$', response.url).groups()
            base_url = "http://www.xicidaili.com/" + data
            if int(page) < 5:
                url = "%s/%s" % (base_url, int(page) + 1)
                yield scrapy.Request(url=url, callback=self.parse, headers=HEADERS)
            else:
                print("page > 5")
        except Exception as e:
            print(e)