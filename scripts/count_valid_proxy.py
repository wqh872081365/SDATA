# -*- coding: utf-8 -*-
from app.proxy.models import Proxy
from app.proxy.helper import USER_AGENT_LIST, TEST_PROXY_URL
import requests
import time
import random

# def count_valid_proxy():
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
#     print({"http_count": proxy_http.count(), "success_http": success_http, "https_count": proxy_https.count(), "success_https" : success_http})
#
# count_valid_proxy()