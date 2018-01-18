# -*- coding: utf-8 -*-

from django.utils import timezone
from django.conf import settings as sdata_settings

import scrapy
import re
import base64
import logging

from wdata.items import ProxyItem

ANONYMITY_DICT = {
    "Transparent": "0",
    "Anonymous": "1",
    "Distorting": "2",
    "Elite": "2",
}

HTTP_DICT = {
    "HTTP": "0",
    "HTTPS": "1",
    "SOCKS4": "2",
    "SOCKS5": "3",
}

COUNTRY_DICT = {
    "CN": "中国"
}

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Connection": "keep-alive",
    "Host": "proxydb.net",
    "Referer": "http://proxydb.net/",
    "Upgrade-Insecure-Requests": 1,
}


class ProxydbSpider(scrapy.Spider):
    name = "proxydb"

    def start_requests(self):
        urls = [
            "http://proxydb.net/?protocol=https&anonlvl=4&min_uptime=75&max_response_time=5&exclude_gateway=1&country=CN&offset=0",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=HEADERS)

    def parse(self, response):
        sel_list = response.xpath("/html/body/div/div/table/tbody//tr")
        for sel in sel_list:
            script_str = sel.xpath("td[1]/script/text()").extract()[0]
            script_str_sub_list= script_str.split(";")
            if len(script_str_sub_list) > 3:
                _d, _var, script_str_ip_1 = re.match(r"(.|\n)*var (\w*) = '([\d\.]*)'\.split\(''\)\.reverse\(\)\.join\(''\)", script_str_sub_list[0]).groups()
                script_str_ip_1 = script_str_ip_1[::-1]
                _d, _var, script_str_ip_2 = re.match(r"(.|\n)*var (\w*) = atob\('([A-Fa-fx0-9\\]*)'\.replace", script_str_sub_list[1]).groups()
                script_str_ip_2 = "".join(chr(int(data, 16)) for data in script_str_ip_2.split(r"\x")[1:])
                script_str_ip_2 = base64.b64decode(script_str_ip_2).decode("utf-8")
                ip = script_str_ip_1 + script_str_ip_2
                _d, _var, script_str_port = re.match(r"(.|\n)*var (\w*) = (.*)", script_str_sub_list[2]).groups()
                port = eval(script_str_port)

                country = sel.xpath("td[3]/abbr/text()").extract()
                isp = sel.xpath("td[4]/div/text()").extract()
                http = sel.xpath("td[5]/text()").extract()
                anonymity = sel.xpath("td[6]/span/text()").extract()
                delay = sel.xpath("td[8]/span/text()").extract()
                verify_time = sel.xpath("td[11]/span/@title").extract()

                self.log(str([ip, port, anonymity, http, country, isp, delay, verify_time]), logging.INFO)
                print(ip, port, anonymity, http, country, isp, delay, verify_time)

                if ip and port:
                    try:
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
                            "city": "",
                            "isp": " ".join(isp),
                            "delay": " ".join(delay),
                            "verify_time": " ".join(verify_time),
                            "source": "proxydb",
                            "update_time": timezone.localtime(timezone.now()).strftime(sdata_settings.LOG_DATE_FORMAT)
                        }
                        print(proxy)
                        yield proxy
                    except Exception as e:
                        print(e)
                        self.log(e, logging.ERROR)
                        continue
        if sel_list:
            try:
                offset = re.match(r'^.*offset=(\d*)$', response.url).groups()[0]
                base_url = "http://proxydb.net/?protocol=https&anonlvl=4&min_uptime=75&max_response_time=5&exclude_gateway=1&country=CN&offset="
                if int(offset) < 100:
                    url = "%s%s" % (base_url, int(offset) + 15)
                    yield scrapy.Request(url=url, callback=self.parse, headers=HEADERS)
                else:
                    print("offset > 100")
                    self.log("offset > 100", logging.WARNING)
            except Exception as e:
                print(e)
                self.log(e, logging.ERROR)