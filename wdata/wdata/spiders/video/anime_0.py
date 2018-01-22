# -*- coding: utf-8 -*-

from django.utils import timezone
from django.conf import settings as sdata_settings
import scrapy
import re
import json
import traceback
import logging

from wdata.items import BilibiliSeasonItem
from app.logs.add_log import add_spider_log, add_user_log, add_msg
from app.video.helper import list_spider_failed
from app.logs.models import UserLog

LOG_TYPE = "0"

BASE_URL = "https://bangumi.bilibili.com/web_api/season/index_global"
SEASON_URL = "https://bangumi.bilibili.com/jsonp/seasoninfo/%s.ver?callback=seasonListCallback"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Connection": "keep-alive",
    "Host": "bangumi.bilibili.com",
    "Referer": "https://www.bilibili.com/",
    "Upgrade-Insecure-Requests": 1,
}


SPIDER_TYPE = {
    "0": "normal",
    "1": "old user log failed",
    "2": "season list",
}


class BilibiliSeasonSpider(scrapy.Spider):
    name = "BilibiliSeason"

    def __init__(self, job_id, type="0", page=0, old_user_log_id=0, season_id_list="", *args, **kwargs):
        super(BilibiliSeasonSpider, self).__init__(*args, **kwargs)
        self.job_id = job_id
        self.type = type
        self.page = page
        self.old_user_log_id = old_user_log_id
        self.season_id_list = season_id_list
        user_log = add_user_log(project="wdata", spider=self.name, job_id=self.job_id, type=LOG_TYPE, count=0, discription=[])
        self.user_log_id = user_log.id

    def start_requests(self):
        url = "%(base_url)s?page=%(page)s" % {"base_url": BASE_URL, "page": self.page}
        season_url = SEASON_URL

        if self.type in ["1", "2"]:
            try:
                user_log = UserLog.objects.get(id=self.user_log_id)
            except Exception as e:
                print(e)
                self.log(e, logging.ERROR)
                user_log = add_user_log(project="wdata", spider=self.name, job_id=self.job_id, type=LOG_TYPE, count=0, discription=[])
                self.user_log_id = user_log.id
            try:
                if self.type == "1":
                    discription = list_spider_failed(int(self.old_user_log_id), LOG_TYPE)
                else:
                    if self.season_id_list and isinstance(self.season_id_list, (str,)):
                        discription = [int(season_id) for season_id in self.season_id_list.split(",")]
                    else:
                        discription = []
                if discription:
                    user_log.count = len(discription)
                    user_log.logs["discription"] = discription
                    user_log.logs["undone"] = discription[1:]
                    user_log.logs["page"] = 0
                    user_log.logs["pages"] = 1
                    user_log.logs["cur_page"] = 1
                    user_log.status = "1"
                    print(len(discription), discription)
                    self.log("%s %s" % (len(discription), discription), logging.INFO)
                    yield scrapy.Request(url=season_url % (discription[0],), callback=self.season_parse, headers=HEADERS)
                else:
                    user_log = add_msg(user_log=user_log, msg="no failed list", response="")
            except Exception as e:
                print(e)
                self.log(e, logging.ERROR)
                user_log = add_msg(user_log=user_log, msg=traceback.format_exc(), response="", type="bg_msg")
            finally:
                user_log.save(update_fields=['logs', 'count', 'status'])
        else:
            if int(self.page) == 0:
                yield scrapy.Request(url=url, callback=self.parse, headers=HEADERS)
            else:
                yield scrapy.Request(url=BASE_URL, callback=self.base_parse, headers=HEADERS)

    def parse(self, response):
        season_url = SEASON_URL
        try:
            user_log = UserLog.objects.get(id=self.user_log_id)
        except Exception as e:
            print(e)
            self.log(e, logging.ERROR)
            user_log = add_user_log(project="wdata", spider=self.name, job_id=self.job_id, type=LOG_TYPE, count=0, discription=[])
            self.user_log_id = user_log.id
        try:
            if response.status == 200:
                data = response.body.decode("utf-8")
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
                                self.log("%s %s" % (len(season_list), discription), logging.INFO)
                                # for season_id in discription:
                                yield scrapy.Request(url=season_url % (discription[0],), callback=self.season_parse, headers=HEADERS)
                            else:
                                user_log = add_msg(user_log=user_log, msg="no season_id", response=response)
                        else:
                            user_log = add_msg(user_log=user_log, msg="season_list is null", response=response)
                    else:
                        user_log = add_msg(user_log=user_log, msg="result is null", response=response)
                else:
                    user_log = add_msg(user_log=user_log, msg="response body is null", response=response)
            else:
                user_log = add_msg(user_log=user_log, msg="response status %s" % (response.status,), response=response)
        except Exception as e:
            print(e)
            self.log(e, logging.ERROR)
            user_log = add_msg(user_log=user_log, msg=traceback.format_exc(), response=response, type="bg_msg")
        finally:
            user_log.save(update_fields=['logs', 'count', 'status'])

    def base_parse(self, response):
        try:
            user_log = UserLog.objects.get(id=self.user_log_id)
        except Exception as e:
            print(e)
            self.log(e, logging.ERROR)
            user_log = add_user_log(project="wdata", spider=self.name, job_id=self.job_id, type=LOG_TYPE, count=0, discription=[])
            self.user_log_id = user_log.id
        try:
            if response.status == 200:
                data = response.body.decode("utf-8")
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
                            self.log("%s %s" % (count, pages), logging.INFO)
                            # for page in range(pages):
                            url = "%(base_url)s?page=%(page)s" % {"base_url": BASE_URL, "page": 1}
                            yield scrapy.Request(url=url, callback=self.sub_parse, headers=HEADERS)
                        else:
                            user_log = add_msg(user_log=user_log, msg="pages or count is null", response=response)
                    else:
                        user_log = add_msg(user_log=user_log, msg="result is null", response=response)
                else:
                    user_log = add_msg(user_log=user_log, msg="response body is null", response=response)
            else:
                user_log = add_msg(user_log=user_log, msg="response status %s" % (response.status,), response=response)
        except Exception as e:
            print(e)
            self.log(e, logging.ERROR)
            user_log = add_msg(user_log=user_log, msg=traceback.format_exc(), response=response, type="bg_msg")
        finally:
            user_log.save(update_fields=['logs', 'count', 'status'])

    def sub_parse(self, response):
        season_url = SEASON_URL
        try:
            user_log = UserLog.objects.get(id=self.user_log_id)
        except Exception as e:
            raise(e)
        try:
            if response.status == 200:
                data = response.body.decode("utf-8")
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
                                    user_log.logs["undone"] = discription[::]
                                print(len(season_list), discription)
                                self.log("%s %s" % (len(season_list), discription), logging.INFO)
                                # for season_id in discription:
                                new_season_id = user_log.logs["undone"].pop(0)
                                yield scrapy.Request(url=season_url % (new_season_id,), callback=self.season_parse, headers=HEADERS)
                            else:
                                user_log = add_msg(user_log=user_log, msg="no season_id", response=response)
                        else:
                            user_log = add_msg(user_log=user_log, msg="season_list is null", response=response)
                    else:
                        user_log = add_msg(user_log=user_log, msg="result is null", response=response)
                else:
                    user_log = add_msg(user_log=user_log, msg="response body is null", response=response)
            else:
                user_log = add_msg(user_log=user_log, msg="response status %s" % (response.status,), response=response)
        except Exception as e:
            print(e)
            self.log(e, logging.ERROR)
            user_log = add_msg(user_log=user_log, msg=traceback.format_exc(), response=response, type="bg_msg")
        finally:
            user_log.save(update_fields=['logs',])

    def season_parse(self, response):
        season_url_next = SEASON_URL
        _season_id = re.match(r'.*seasoninfo/(\d*)', response.url).groups()
        try:
            user_log = UserLog.objects.get(id=self.user_log_id)
        except Exception as e:
            raise(e)
        if _season_id:
            source_id = int(_season_id[0])
            try:
                if response.status == 200:
                    data = re.match(r'^seasonListCallback\(([\s\S]*)\);$', response.body.decode("utf-8")).groups()
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

                            print(season)

                            if user_log.logs["undone"]:
                                season["complete"] = False
                                yield season
                                new_season_id = user_log.logs["undone"].pop(0)
                                yield scrapy.Request(url=season_url_next % (new_season_id,), callback=self.season_parse, headers=HEADERS)
                            else:
                                if user_log.logs["cur_page"] < user_log.logs["pages"]:
                                    season["complete"] = False
                                    yield season
                                    user_log.logs["cur_page"] += 1
                                    url = "%(base_url)s?page=%(page)s" % {"base_url": BASE_URL, "page": user_log.logs["cur_page"]}
                                    yield scrapy.Request(url=url, callback=self.sub_parse, headers=HEADERS)
                                else:
                                    season["complete"] = True
                                    user_log.status = "2"
                                    yield season
                        else:
                            add_spider_log(user_log_id=user_log.id, source=LOG_TYPE, source_id=source_id, url=response.url, status="3", msg="result is null", response=response)
                    else:
                        add_spider_log(user_log_id=user_log.id, source=LOG_TYPE, source_id=source_id, url=response.url, status="2", msg="response body is not verify", response=response)
                else:
                    add_spider_log(user_log_id=user_log.id, source=LOG_TYPE, source_id=source_id, url=response.url, status="0", msg="response status %s" % (response.status,), response=response)
            except Exception as e:
                print(e)
                self.log(e, logging.ERROR)
                add_spider_log(user_log_id=user_log.id, source=LOG_TYPE, source_id=source_id, url=response.url, status="4", msg=traceback.format_exc(), response=response, type="bg_msg")
            finally:
                user_log.save(update_fields=['status', 'logs'])
        else:
            print(response.url)
            self.log(response.url, logging.WARNING)