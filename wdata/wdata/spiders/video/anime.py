# -*- coding: utf-8 -*-

from django.utils import timezone
from django.conf import settings as sdata_settings
import scrapy
import re
import json
import traceback

from wdata.items import BilibiliSeasonItem
from app.logs.add_log import add_spider_log, add_user_log
from app.logs.models import UserLog

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
        user_log = add_user_log(type="0", count=0, discription=[])
        self.user_log_id = user_log.id

    def start_requests(self):
        url = "%(base_url)s?page=%(page)s" % {"base_url": BASE_URL, "page": self.page}

        if int(self.page) == 0:
            yield scrapy.Request(url=url, callback=self.parse, headers=HEADERS)
        else:
            yield scrapy.Request(url=BASE_URL, callback=self.base_parse, headers=HEADERS)

    def parse(self, response):
        season_url = "https://bangumi.bilibili.com/jsonp/seasoninfo/%s.ver?callback=seasonListCallback"
        try:
            user_log = UserLog.objects.get(id=self.user_log_id)
        except Exception as e:
            print(e)
            user_log = add_user_log(type="0", count=0, discription=[])
            self.user_log_id = user_log.id
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
                                user_log.count = len(discription)
                                user_log.logs["discription"] = discription
                                user_log.logs["undone"] = discription[1:]
                                user_log.logs["page"] = int(self.page)
                                user_log.logs["pages"] = 1
                                user_log.logs["cur_page"] = 1
                                user_log.status = "1"
                                print(len(season_list), discription)
                                # for season_id in discription:
                                yield scrapy.Request(url=season_url % (discription[0],), callback=self.season_parse, headers=HEADERS)
                            else:
                                user_log.add_msg(msg="no season_id", response=response)
                        else:
                            user_log.add_msg(msg="season_list is null", response=response)
                    else:
                        user_log.add_msg(msg="result is null", response=response)
                else:
                    user_log.add_msg(msg="response body is null", response=response)
            else:
                user_log.add_msg(msg="response status %s" % (response.status,), response=response)
        except Exception as e:
            print(e)
            user_log.add_msg(msg=traceback.format_exc(), response=response, type="bg_msg")
        finally:
            user_log.save()

    def base_parse(self, response):
        try:
            user_log = UserLog.objects.get(id=self.user_log_id)
        except Exception as e:
            print(e)
            user_log = add_user_log(type="0", count=0, discription=[])
            self.user_log_id = user_log.id
        try:
            if response.status == 200:
                data = response.body
                if data:
                    result = json.loads(data).get("result", {})
                    if result:
                        count = int(result.get("count", "0"))
                        pages = int(result.get("pages", "1"))
                        if pages and count:
                            user_log.count = count
                            user_log.logs["page"] = int(self.page)
                            user_log.logs["pages"] = pages
                            user_log.logs["cur_page"] = 1
                            user_log.status = "1"
                            print(count, pages)
                            # for page in range(pages):
                            url = "%(base_url)s?page=%(page)s" % {"base_url": BASE_URL, "page": 1}
                            yield scrapy.Request(url=url, callback=self.sub_parse, headers=HEADERS)
                        else:
                            user_log.add_msg(msg="pages or count is null", response=response)
                    else:
                        user_log.add_msg(msg="result is null", response=response)
                else:
                    user_log.add_msg(msg="response body is null", response=response)
            else:
                user_log.add_msg(msg="response status %s" % (response.status,), response=response)
        except Exception as e:
            print(e)
            user_log.add_msg(msg=traceback.format_exc(), response=response, type="bg_msg")
        finally:
            user_log.save()

    def sub_parse(self, response):
        season_url = "https://bangumi.bilibili.com/jsonp/seasoninfo/%s.ver?callback=seasonListCallback"
        try:
            user_log = UserLog.objects.get(id=self.user_log_id)
        except Exception as e:
            raise(e)
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
                                if user_log.logs["discription"]:
                                    user_log.logs["discription"] += discription
                                    user_log.logs["undone"] += discription
                                else:
                                    user_log.logs["discription"] = discription
                                    user_log.logs["undone"] = discription
                                print(len(season_list), discription)
                                # for season_id in discription:
                                new_season_id = user_log.logs["undone"].pop(0)
                                yield scrapy.Request(url=season_url % (new_season_id,), callback=self.season_parse, headers=HEADERS)
                            else:
                                user_log.add_msg(msg="no season_id", response=response)
                        else:
                            user_log.add_msg(msg="season_list is null", response=response)
                    else:
                        user_log.add_msg(msg="result is null", response=response)
                else:
                    user_log.add_msg(msg="response body is null", response=response)
            else:
                user_log.add_msg(msg="response status %s" % (response.status,), response=response)
        except Exception as e:
            print(e)
            user_log.add_msg(msg=traceback.format_exc(), response=response, type="bg_msg")
        finally:
            user_log.save()

    def season_parse(self, response):
        season_url_next = "https://bangumi.bilibili.com/jsonp/seasoninfo/%s.ver?callback=seasonListCallback"
        _season_id = re.match(r'.*seasoninfo/(\d*)', response.url).groups()
        try:
            user_log = UserLog.objects.get(id=self.user_log_id)
        except Exception as e:
            raise(e)
        if _season_id:
            source_id = int(_season_id[0])
            try:
                if response.status == 200:
                    data = re.match(r'^seasonListCallback\(([\s\S]*)\);$', response.body).groups()
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
                            detail = {"data": result, "time": timezone.localtime(timezone.now()).strftime(sdata_settings.LOG_DATE_FORMAT), "user_log_id": user_log.id}
                            season = BilibiliSeasonItem()
                            season["season_id"] = int(season_id)
                            season["season_name"] = season_name
                            season["bangumi_id"] = int(bangumi_id)
                            season["bangumi_name"] = bangumi_name
                            season["season_url"] = season_url
                            season["play_count"] = int(play_count)
                            season["detail"] = detail
                            season["status"] = status

                            user_log.success += 1
                            if user_log.success == user_log.count:
                                user_log.status = "2"
                                user_log.add_end()
                            print(season)
                            yield season
                            if user_log.logs["undone"]:
                                if len(user_log.logs["undone"]) == len(user_log.logs["discription"]) - 1:
                                    new_season_id = user_log.logs["undone"].pop(0)
                                    yield scrapy.Request(url=season_url_next % (new_season_id,), callback=self.season_parse, headers=HEADERS)
                            else:
                                if user_log.logs["cur_page"] < user_log.logs["pages"]:
                                    user_log.logs["cur_page"] += 1
                                    url = "%(base_url)s?page=%(page)s" % {"base_url": BASE_URL, "page": user_log.logs["cur_page"]}
                                    yield scrapy.Request(url=url, callback=self.sub_parse, headers=HEADERS)
                        else:
                            add_spider_log(user_log_id=user_log.id, source="0", source_id=source_id, url=response.url, status="3", msg="result is null", response=response)
                    else:
                        add_spider_log(user_log_id=user_log.id, source="0", source_id=source_id, url=response.url, status="2", msg="response body is not verify", response=response)
                else:
                    add_spider_log(user_log_id=user_log.id, source="0", source_id=source_id, url=response.url, status="0", msg="response status %s" % (response.status,), response=response)
            except Exception as e:
                print(e)
                add_spider_log(user_log_id=user_log.id, source="0", source_id=source_id, url=response.url, status="4", msg=traceback.format_exc(), response=response, type="bg_msg")
            finally:
                user_log.save()
        else:
            print(response.url)