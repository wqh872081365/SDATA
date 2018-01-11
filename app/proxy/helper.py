# -*- coding: utf-8 -*-

from app.proxy.models import Proxy

import requests
import time
import random

TEST_PROXY_URL = {
    "https": "https://www.baidu.com",
    # "http": "http://www.xicidaili.com"
}

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
]


def get_random_proxy(**kwargs):
    return Proxy.objects.filter(**kwargs).order_by("?").first()


# def get_valid_proxy_number():
#     proxy_http = Proxy.objects.filter(anonymity="2", country="中国", http="0", status__in=["1", "2"])
#     proxy_https = Proxy.objects.filter(anonymity="2", country="中国", http="1", status__in=["1", "2"])
#     success_http = 0
#     success_https = 0
#     for proxy in proxy_http:
#         try:
#             r = requests.get(TEST_PROXY_URL.get("http"), proxies={"http": "%s://%s:%s" % ("http", proxy.ip, proxy.port)}, headers={"User-Agent": random.choice(USER_AGENT_LIST)})
#             time.sleep(1)
#             if r.status_code == 200:
#                 success_http += 1
#                 if proxy.status == "2":
#                     proxy.status = "1"
#                     proxy.save()
#             else:
#                 proxy.status = "0"
#                 proxy.save()
#         except Exception as e:
#             print(e)
#             proxy.status = "0"
#             proxy.save()
#             continue
#     for proxy in proxy_https:
#         try:
#             r = requests.get(TEST_PROXY_URL.get("https"), proxies={"https": "%s://%s:%s" % ("https", proxy.ip, proxy.port)}, headers={"User-Agent": random.choice(USER_AGENT_LIST)})
#             time.sleep(1)
#             if r.status_code == 200:
#                 success_https += 1
#                 if proxy.status == "2":
#                     proxy.status = "1"
#                     proxy.save()
#             else:
#                 proxy.status = "0"
#                 proxy.save()
#         except Exception as e:
#             print(e)
#             proxy.status = "0"
#             proxy.save()
#             continue
#     return {"http_count": proxy_http.count(), "success_http": success_http, "https_count": proxy_https.count(), "success_https" : success_http}