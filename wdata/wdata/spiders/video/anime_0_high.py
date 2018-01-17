# -*- coding: utf-8 -*-

from django.utils import timezone
from django.conf import settings as sdata_settings
import scrapy
import re
import json
import traceback

from wdata.items import BilibiliSeasonItem
from app.logs.add_log import add_spider_log, add_user_log, add_msg, add_end
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


class BilibiliSeasonHighSpider(scrapy.Spider):
    name = "BilibiliSeasonHigh"

    def __init__(self, type="0", page=0, old_user_log_id=0, season_id_list="", *args, **kwargs):
        super(BilibiliSeasonHighSpider, self).__init__(*args, **kwargs)
        self.type = type
        self.page = page
        self.old_user_log_id = old_user_log_id
        self.season_id_list = season_id_list
        user_log = add_user_log(type=LOG_TYPE, count=0, discription=[])
        self.user_log_id = user_log.id

    def start_requests(self):
        url = "%(base_url)s?page=%(page)s" % {"base_url": BASE_URL, "page": 0}
        season_url = SEASON_URL

        if self.type in ["1", "2"]:
            try:
                user_log = UserLog.objects.get(id=self.user_log_id)
            except Exception as e:
                print(e)
                user_log = add_user_log(type=LOG_TYPE, count=0, discription=[])
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
                    user_log.logs["undone"] = []
                    user_log.logs["page"] = 0
                    user_log.logs["pages"] = 1
                    user_log.logs["cur_page"] = 1
                    user_log.status = "1"
                    user_log.save(update_fields=['logs', 'count', 'status'])
                    print(len(discription), discription)
                    for season_id in discription:
                        try:
                            yield scrapy.Request(url=season_url % (season_id,), callback=self.season_parse, headers=HEADERS)
                        except Exception as e:
                            print(e)
                            continue
                else:
                    print("no failed list")
                    # user_log = add_msg(user_log=user_log, msg="no failed list", response="")
            except Exception as e:
                print(e)
                # user_log = add_msg(user_log=user_log, msg=traceback.format_exc(), response="", type="bg_msg")
            finally:
                pass
        else:
            yield scrapy.Request(url=url, callback=self.parse, headers=HEADERS)

    def parse(self, response):
        season_url = SEASON_URL
        try:
            user_log = UserLog.objects.get(id=self.user_log_id)
        except Exception as e:
            print(e)
            user_log = add_user_log(type=LOG_TYPE, count=0, discription=[])
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
                                user_log.logs["undone"] = []
                                user_log.logs["page"] = 0
                                user_log.logs["pages"] = 1
                                user_log.logs["cur_page"] = 1
                                user_log.status = "1"
                                user_log.save(update_fields=['logs', 'count', 'status'])
                                print(len(season_list), discription)
                                for season_id in discription:
                                    try:
                                        yield scrapy.Request(url=season_url % (season_id,), callback=self.season_parse, headers=HEADERS)
                                    except Exception as e:
                                        print(e)
                                        continue
                            else:
                                print("no season_id")
                                # user_log = add_msg(user_log=user_log, msg="no season_id", response=response)
                        else:
                            print("season_list is null")
                            # user_log = add_msg(user_log=user_log, msg="season_list is null", response=response)
                    else:
                        print("result is null")
                        # user_log = add_msg(user_log=user_log, msg="result is null", response=response)
                else:
                    print("response body is null")
                    # user_log = add_msg(user_log=user_log, msg="response body is null", response=response)
            else:
                print("response status %s" % (response.status,))
                # user_log = add_msg(user_log=user_log, msg="response status %s" % (response.status,), response=response)
        except Exception as e:
            print(e)
            # user_log = add_msg(user_log=user_log, msg=traceback.format_exc(), response=response, type="bg_msg")
        finally:
            pass

    def season_parse(self, response):
        _season_id = re.match(r'.*seasoninfo/(\d*)', response.url).groups()
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
                            detail = {"data": result, "time": timezone.localtime(timezone.now()).strftime(sdata_settings.LOG_DATE_FORMAT), "user_log_id": self.user_log_id}
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
                        else:
                            print("result is null")
                            # add_spider_log(user_log_id=self.user_log_id, source=LOG_TYPE, source_id=source_id, url=response.url, status="3", msg="result is null", response=response)
                    else:
                        print("response body is not verify")
                        # add_spider_log(user_log_id=self.user_log_id, source=LOG_TYPE, source_id=source_id, url=response.url, status="2", msg="response body is not verify", response=response)
                else:
                    print("response status %s" % (response.status,))
                    # add_spider_log(user_log_id=self.user_log_id, source=LOG_TYPE, source_id=source_id, url=response.url, status="0", msg="response status %s" % (response.status,), response=response)
            except Exception as e:
                print(e)
                # add_spider_log(user_log_id=self.user_log_id, source=LOG_TYPE, source_id=source_id, url=response.url, status="4", msg=traceback.format_exc(), response=response, type="bg_msg")
            finally:
                pass
        else:
            print(response.url)