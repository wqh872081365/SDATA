# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from django.core.validators import validate_ipv46_address
from django.utils import timezone
from django.conf import settings as sdata_settings

import traceback

from app.proxy.models import Proxy
from app.video.models import BilibiliSeason
from app.logs.models import UserLog
from app.logs.add_log import add_msg, update_user_log

from wdata.items import ProxyItem, BilibiliSeasonItem


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
                    if proxy.status == "0":
                        proxy.status = "2"
                    # proxy.modified = timezone.now()
                    proxy.save()
                else:
                    country = item["country"][:100]
                    source = item["detail"].get("source", "")
                    Proxy.objects.create(ip=ip, port=port, source=source, anonymity=item["anonymity"], country=country, http=item["http"], status="2", detail={"details": [item["detail"]]}, success_count=0, failure_count=0)
            except Exception as e:
                print(e)
        elif type(item) == BilibiliSeasonItem:
            if spider.name == "BilibiliSeasonHigh":
                season_id = item["season_id"]
                user_log_id = item["detail"].get("user_log_id")
                try:
                    if BilibiliSeason.objects.filter(season_id=season_id):
                        season = BilibiliSeason.objects.get(season_id=season_id)
                        season.play_count = item["play_count"]
                        # season.detail["details"].append(item["detail"])
                        season.detail["details"].append({"data": {"coins": item["detail"].get("data", {}).get("coins", ""), "favorites": item["detail"].get("data", {}).get("favorites", ""), "play_count": item["detail"].get("data", {}).get("play_count", ""), "danmaku_count": item["detail"].get("data", {}).get("danmaku_count", "")}, "time": timezone.localtime(timezone.now()).strftime(sdata_settings.LOG_DATE_FORMAT), "user_log_id": user_log_id})
                        season.save()
                    else:
                        season_name = item["season_name"][:100]
                        bangumi_name = item["bangumi_name"][:100]
                        BilibiliSeason.objects.create(season_id=season_id, season_name=season_name, bangumi_id=item["bangumi_id"], bangumi_name=bangumi_name, season_url=item["season_url"], play_count=item["play_count"], status=item["status"], detail={"details": [item["detail"]]})
                except Exception as e:
                    print(e)
                finally:
                    pass
            else:
                season_id = item["season_id"]
                user_log_id = item["detail"].get("user_log_id")
                try:
                    user_log = UserLog.objects.get(id=user_log_id)
                except Exception as e:
                    raise (e)
                try:
                    if BilibiliSeason.objects.filter(season_id=season_id):
                        season = BilibiliSeason.objects.get(season_id=season_id)
                        season.play_count = item["play_count"]
                        # season.detail["details"].append(item["detail"])
                        season.detail["details"].append({"data": {"coins": item["detail"].get("data", {}).get("coins", ""), "favorites": item["detail"].get("data", {}).get("favorites", ""), "play_count": item["detail"].get("data", {}).get("play_count", ""), "danmaku_count": item["detail"].get("data", {}).get("danmaku_count", "")}, "time": timezone.localtime(timezone.now()).strftime(sdata_settings.LOG_DATE_FORMAT), "user_log_id": user_log.id})
                        season.save()
                    else:
                        season_name = item["season_name"][:100]
                        bangumi_name = item["bangumi_name"][:100]
                        BilibiliSeason.objects.create(season_id=season_id, season_name=season_name, bangumi_id=item["bangumi_id"], bangumi_name=bangumi_name, season_url=item["season_url"], play_count=item["play_count"], status=item["status"], detail={"details": [item["detail"]]})
                    if user_log.success_detail.get("success") and isinstance(user_log.success_detail["success"], (tuple, list)):
                        user_log.success_detail["success"].append(season_id)
                    else:
                        user_log.success_detail["success"] = [season_id, ]
                    if item["complete"]:
                        if len(user_log.success_detail["success"]) == len(user_log.logs["discription"]):
                            user_log.success_detail["complete"] = True
                        else:
                            user_log.success_detail["complete"] = False
                except Exception as e:
                    print(e)
                    user_log = add_msg(user_log=user_log, msg=traceback.format_exc(), response=item.items(), type="bg_msg", source="pipeline")
                finally:
                    user_log.save(update_fields=['success_detail', ])
        return item