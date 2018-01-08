"""Set User-Agent header per spider or use a default value from settings"""

from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import random
import requests

from app.proxy.helper import get_random_proxy
from app.utils.scrapy import add_schedule, PROXY_LIST, JOB_DICT, PROXY_HOST_LIST

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
]

from app.proxy.helper import TEST_PROXY_URL


class UserAgentMiddleware(object):
    """This middleware allows spiders to override the user_agent"""

    def __init__(self, user_agent='Scrapy'):
        self.user_agent = random.choice(USER_AGENT_LIST)

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER_AGENT'])
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent', self.user_agent)

    def process_request(self, request, spider):
        if self.user_agent:
            request.headers.setdefault(b'User-Agent', self.user_agent)


class RandomHttpProxyMiddleware(HttpProxyMiddleware):

    def _set_proxy(self, request, scheme):
        if request.headers.get("Host") not in PROXY_HOST_LIST:
            index = 0
            while 1:
                index += 1
                if index > 10:
                    proxy_site = random.choice(PROXY_LIST)
                    add_schedule("wdata", proxy_site, JOB_DICT.ge(proxy_site))
                if index > 100:
                    raise("too much invalid proxy")
                try:
                    if scheme == "https":
                        proxy = get_random_proxy(anonymity="2", country="中国", http="1", status="1")
                        r = requests.get(TEST_PROXY_URL.get("https"), proxies={"https": "%s://%s:%s" % ("https", proxy.ip, proxy.port)}, headers={"User-Agent": random.choice(USER_AGENT_LIST)})
                    else:
                        proxy = get_random_proxy(anonymity="2", country="中国", http="0", status="1")
                        r = requests.get(TEST_PROXY_URL.get("http"), proxies={"http": "%s://%s:%s" % ("http", proxy.ip, proxy.port)}, headers={"User-Agent": random.choice(USER_AGENT_LIST)})
                except Exception as e:
                    print(e)
                    proxy.status = "0"
                    proxy.save()
                    continue
                if r.status_code == 200:
                    break
                else:
                    proxy.status = "0"
                    proxy.save()
            creds, _ = self.proxies[scheme]
            request.meta['proxy'] = "%s://%s:%s" % (scheme, proxy.ip, proxy.port)
            if creds:
                request.headers['Proxy-Authorization'] = b'Basic ' + creds