# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from django.core.validators import validate_ipv46_address
from django.utils import timezone

from app.proxy.models import Proxy

from wdata.items import ProxyItem


class WdataPipeline(object):
    def process_item(self, item, spider):
        return item


class PostgresPipeline(object):
    def process_item(self, item, spider):
        if type(item) == ProxyItem:
            ip = item["ip"]
            port = item["port"]
            try:
                validate_ipv46_address(ip)
                if Proxy.objects.filter(ip=ip, port=port):
                    proxy = Proxy.objects.get(ip=ip, port=port)
                    proxy.detail["details"].append(item["detail"])
                    proxy.modified = timezone.now()
                    proxy.save()
                else:
                    country = item["country"][:100]
                    Proxy.objects.create(ip=ip, port=port, source="data5u", anonymity=item["anonymity"], country=country, http=item["http"], status="2", detail={"details": [item["detail"]]}, success_count=0, failure_count=0, created=timezone.now(), modified=timezone.now())
            except Exception as e:
                print(e)
        return item