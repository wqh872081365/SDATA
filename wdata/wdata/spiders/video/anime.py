# -*- coding: utf-8 -*-

from django.utils import timezone
import scrapy
import re
import json
import traceback

from wdata.items import BilibiliSeasonItem
from app.logs.add_log import add_spider_log, add_user_log

BASE_URL = "https://bangumi.bilibili.com/web_api/season/index_global"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Connection": "keep-alive",
    "Host": "bangumi.bilibili.com",
    "Referer": "https://www.bilibili.com/",
    "Upgrade-Insecure-Requests": 1,
}


class BilibiliSeasonSpider(scrapy.Spider):
    name = "BilibiliSeason"

    def __init__(self, page=0, *args, **kwargs):
        super(BilibiliSeasonSpider, self).__init__(*args, **kwargs)
        self.page = page
        self.user_log = add_user_log(type="0", count=0, discription=[])

    def start_requests(self):
        url = "%(base_url)s?page=%(page)s" % {"base_url": BASE_URL, "page": self.page}

        if int(self.page) == 0:
            yield scrapy.Request(url=url, callback=self.parse, headers=HEADERS)
        else:
            yield scrapy.Request(url=BASE_URL, callback=self.base_parse, headers=HEADERS)

    def parse(self, response):
        season_url = "https://bangumi.bilibili.com/jsonp/seasoninfo/%s.ver"
        try:
            if response.status == 200:
                data = response.body
                if data:
                    result = json.loads(data).get("result", {})
                    if result:
                        season_list = result.get("list", [])
                        if season_list:
                            discription = [int(season.get("season_id")) for season in season_list if season.get("season_id")]
                            if discription:
                                self.user_log.count = len(discription)
                                self.user_log.logs["discription"] = discription
                                self.user_log.logs["page"] = int(self.page)
                                self.user_log.status = "1"
                                print(len(season_list), discription)
                                for season_id in discription:
                                    yield scrapy.Request(url=season_url % (season_id,), callback=self.season_parse, headers=HEADERS)
                            else:
                                self.user_log.add_msg(msg="no season_id", response=response)
                        else:
                            self.user_log.add_msg(msg="season_list is null", response=response)
                    else:
                        self.user_log.add_msg(msg="result is null", response=response)
                else:
                    self.user_log.add_msg(msg="response body is null", response=response)
            else:
                self.user_log.add_msg(msg="response status %s" % (response.status,), response=response)
        except Exception as e:
            print(e)
            self.user_log.add_msg(msg=e, response=response)
            self.user_log.add_msg(msg=traceback.format_exc(), response=response, type="bg_msg")
        finally:
            self.user_log.save()

    def base_parse(self, response):
        try:
            if response.status == 200:
                data = response.body
                if data:
                    result = json.loads(data).get("result", {})
                    if result:
                        count = int(result.get("count", "0"))
                        pages = int(result.get("pages", "1"))
                        if pages and count:
                            self.user_log.count = count
                            self.user_log.logs["page"] = int(self.page)
                            print(count, pages)
                            for page in range(pages):
                                url = "%(base_url)s?page=%(page)s" % {"base_url": BASE_URL, "page": page + 1}
                                yield scrapy.Request(url=url, callback=self.sub_parse, headers=HEADERS)
                        else:
                            self.user_log.add_msg(msg="pages or count is null", response=response)
                    else:
                        self.user_log.add_msg(msg="result is null", response=response)
                else:
                    self.user_log.add_msg(msg="response body is null", response=response)
            else:
                self.user_log.add_msg(msg="response status %s" % (response.status,), response=response)
        except Exception as e:
            print(e)
            self.user_log.add_msg(msg=e, response=response)
            self.user_log.add_msg(msg=traceback.format_exc(), response=response, type="bg_msg")
        finally:
            self.user_log.save()

    def sub_parse(self, response):
        season_url = "https://bangumi.bilibili.com/jsonp/seasoninfo/%s.ver"
        try:
            if response.status == 200:
                data = response.body
                if data:
                    result = json.loads(data).get("result", {})
                    if result:
                        season_list = result.get("list", [])
                        if season_list:
                            discription = [int(season.get("season_id")) for season in season_list if season.get("season_id")]
                            if discription:
                                if self.user_log.logs["discription"]:
                                    self.user_log.logs["discription"] += discription
                                else:
                                    self.user_log.logs["discription"] = discription
                                if self.user_log.status == "5":
                                    self.user_log.status = "1"
                                print(len(season_list), discription)
                                for season_id in discription:
                                    yield scrapy.Request(url=season_url % (season_id,), callback=self.season_parse, headers=HEADERS)
                            else:
                                self.user_log.add_msg(msg="no season_id", response=response)
                        else:
                            self.user_log.add_msg(msg="season_list is null", response=response)
                    else:
                        self.user_log.add_msg(msg="result is null", response=response)
                else:
                    self.user_log.add_msg(msg="response body is null", response=response)
            else:
                self.user_log.add_msg(msg="response status %s" % (response.status,), response=response)
        except Exception as e:
            print(e)
            self.user_log.add_msg(msg=e, response=response)
            self.user_log.add_msg(msg=traceback.format_exc(), response=response, type="bg_msg")
        finally:
            self.user_log.save()

    def season_parse(self, response):
        _season_id = re.match(r'^https://bangumi.bilibili.com/jsonp/seasoninfo/(\d*).ver$', response.url).groups()
        if _season_id:
            source_id = int(_season_id[0])
            spider_log = add_spider_log(user_log_id=self.user_log.id, source="0", source_id=source_id, url=response.url)
            try:
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
                            status = True
                            if not season_id:
                                season_id = source_id
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

                            self.user_log.success += 1
                            if self.user_log.success == self.user_log.count:
                                self.user_log.status = "2"
                                self.user_log.add_end()
                            self.user_log.save()

                            spider_log.status = "1"

                            print(season)
                            yield season
                        else:
                            spider_log.add_msg(msg="result is null", response=response)
                    else:
                        spider_log.add_msg(msg="response body is not verify", response=response)
                else:
                    spider_log.add_msg(msg="response status %s" % (response.status,), response=response)
            except Exception as e:
                print(e)
                spider_log.add_msg(msg=e, response=response)
                spider_log.add_msg(msg=traceback.format_exc(), response=response, type="bg_msg")
            finally:
                spider_log.save()
        else:
            print(response.url)