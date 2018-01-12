"""Set User-Agent header per spider or use a default value from settings"""

from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware, urlparse_cached
import random
import requests
import time

from django.conf import settings as sdata_settings

from app.proxy.helper import get_random_proxy
from app.utils.scrapy import add_schedule, PROXY_LIST, JOB_DICT, PROXY_NAME_LIST
from app.proxy.helper import USER_AGENT_LIST


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

    def process_request(self, request, spider):
        parsed = urlparse_cached(request)
        scheme = parsed.scheme
        if spider.name not in PROXY_NAME_LIST and scheme in ('http', 'https'):
            index = 0
            # spider_start = False
            while 1:
                index += 1
                # if index > 10 and not spider_start:
                #     proxy_site = random.choice(PROXY_LIST)
                #     add_schedule("wdata", proxy_site, JOB_DICT.get(proxy_site))
                #     spider_start = True
                #     time.sleep(10)
                if index > 100:
                    raise("too much invalid proxy")
                try:
                    # if scheme == "https":
                    proxy = get_random_proxy(anonymity="2", country="中国", http="1", status="1")
                    r = requests.get(TEST_PROXY_URL.get("https"), proxies={"https": "%s://%s:%s" % ("https", proxy.ip, proxy.port)}, headers={"User-Agent": random.choice(USER_AGENT_LIST)}, timeout=sdata_settings.SPIDER_TIMEOUT)
                    # else:
                    #     proxy = get_random_proxy(anonymity="2", country="中国", http="0", status="1")
                    #     r = requests.get(TEST_PROXY_URL.get("http"), proxies={"http": "%s://%s:%s" % ("http", proxy.ip, proxy.port)}, headers={"User-Agent": random.choice(USER_AGENT_LIST)})
                except Exception as e:
                    print(e)
                    # proxy.status = "0"
                    # proxy.save()
                    continue
                if r.status_code == 200:
                    print("user proxy %s:%s" % (proxy.ip, proxy.port))
                    break
                else:
                    # proxy.status = "0"
                    # proxy.save()
                    pass
            request.meta['proxy'] = "%s://%s:%s" % (scheme, proxy.ip, proxy.port)
