# -*- coding: utf-8 -*-

from django.utils import timezone
import scrapy
import re
import json

from wdata.items import BilibiliSeasonItem
from app.logs.models import SpiderLog


class BilibiliSeasonSpider(scrapy.Spider):
    name = "BilibiliSeason"

    def start_requests(self):
        url = "https://bangumi.bilibili.com/jsonp/seasoninfo/%s.ver"

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
            "Connection": "keep-alive",
            "Host": "bangumi.bilibili.com",
            "Referer": "",
            "Upgrade-Insecure-Requests": 1,
        }

        yield scrapy.Request(url=url % (6439,), callback=self.parse, headers=headers)

    def parse(self, response):
        spider_log = SpiderLog(user_log_id=1, source="0", source_id=0, url="", status="-1", logs={})
        spider_log.save()

        if response.status == 200:
            data = re.match(r'^seasonListCallback\((.*)\);$', response.body).groups()
            if data:
                result = json.loads(data[0]).get("result", {})
                if result:
                    season_id = result.get("season_id", 0)
                    season_name = result.get("season_title", "")
                    bangumi_id = result.get("bangumi_id", 0)
                    bangumi_name = result.get("bangumi_title", "")
                    season_url = result.get("share_url", "")
                    play_count = result.get("play_count", 0)
                    if season_id:
                        status = True
                    else:
                        status = False

                    spider_log.source_id = season_id
                    spider_log.url = response.url
                    spider_log.status = ""
                    spider_log.logs = {}
                    spider_log.save()

                    detail = {"data": result, "time": timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"), "log_id": spider_log.id}
                    season = BilibiliSeasonItem()
                    season["season_id"] = int(season_id)
                    season["season_name"] = season_name
                    season["bangumi_id"] = int(bangumi_id)
                    season["bangumi_name"] = bangumi_name
                    season["season_url"] = season_url
                    season["play_count"] = int(play_count)
                    season["detail"] = detail
                    season["status"] = status
                    print(season)
                    yield season