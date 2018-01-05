# -*- coding: utf-8 -*-

from app.proxy.models import Proxy

import requests

TEST_PROXY_URL = ""


def get_random_proxy(**kwargs):
    return Proxy.objects.filter(**kwargs).order_by("?").first()


def get_valid_proxy_number():
    proxy_http = get_random_proxy(anonymity="2", country="中国", http="0", status="1")
    proxy_https = get_random_proxy(anonymity="2", country="中国", http="1", status="1")
    success_http = 0
    success_https = 0
    for proxy in proxy_http:
        r = requests.get("http://127.0.0.1:6800", proxies={"http": "%s://%s:%s" % ("http", proxy.ip, proxy.port)})
        if r.status_code == 200:
            success_http += 1
        else:
            proxy.status = "0"
            proxy.save()
    for proxy in proxy_https:
        r = requests.get("https://127.0.0.1:6800", proxies={"https": "%s://%s:%s" % ("https", proxy.ip, proxy.port)})
        if r.status_code == 200:
            success_https += 1
        else:
            proxy.status = "0"
            proxy.save()
    return {"success_http": success_http, "success_https" : success_http}