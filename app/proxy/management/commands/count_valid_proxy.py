# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from app.proxy.models import Proxy
from app.proxy.helper import USER_AGENT_LIST, TEST_PROXY_URL
from app.utils.scrapy import add_schedule, PROXY_LIST, JOB_DICT

import requests
import time
import random


class Command(BaseCommand):

    def handle(self, *args, **options):
        # while 1:
        # proxy_http = Proxy.objects.filter(anonymity="2", country="中国", http="0", status__in=["1", "2"])
        proxy_https = Proxy.objects.filter(anonymity="2", country="中国", http="1", status__in=["1", "2"])
        # success_http = 0
        success_https = 0
        # for proxy in proxy_http:
        #     try:
        #         r = requests.get(TEST_PROXY_URL.get("http"), proxies={"http": "%s://%s:%s" % ("http", proxy.ip, proxy.port)}, headers={"User-Agent": random.choice(USER_AGENT_LIST)}, timeout=5)
        #         time.sleep(1)
        #         if r.status_code == 200:
        #             success_http += 1
        #             if proxy.status == "2":
        #                 proxy.status = "1"
        #                 proxy.save()
        #             print("proxy " + "%s://%s:%s" % ("http", proxy.ip, proxy.port) + " ok")
        #         else:
        #             proxy.status = "0"
        #             proxy.save()
        #             print("proxy " + "%s://%s:%s" % ("http", proxy.ip, proxy.port) + " status " + str(r.status_code))
        #     except Exception as e:
        #         print(e)
        #         proxy.status = "0"
        #         proxy.save()
        #         continue
        for proxy in proxy_https:
            try:
                r = requests.get(TEST_PROXY_URL.get("https"), proxies={"https": "%s://%s:%s" % ("https", proxy.ip, proxy.port)}, headers={"User-Agent": random.choice(USER_AGENT_LIST)}, timeout=settings.SPIDER_TIMEOUT)
                time.sleep(1)
                if r.status_code == 200:
                    success_https += 1
                    if proxy.status == "2":
                        proxy.status = "1"
                        proxy.save()
                    print("proxy " + "%s://%s:%s" % ("https", proxy.ip, proxy.port) + " ok")
                else:
                    proxy.status = "0"
                    proxy.save()
                    print("proxy " + "%s://%s:%s" % ("https", proxy.ip, proxy.port) + " status " + str(r.status_code))
            except Exception as e:
                print("proxy " + "%s://%s:%s" % ("https", proxy.ip, proxy.port) + " failed")
                print(e)
                proxy.status = "0"
                proxy.save()
                continue
        print({"https_count": proxy_https.count(), "success_https": success_https})

        # if success_https < 10:
        #     proxy_site = random.choice(PROXY_LIST)
        #     add_schedule("wdata", proxy_site, JOB_DICT.get(proxy_site))
        #     time.sleep(300)
        # else:
        #     break