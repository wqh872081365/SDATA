# -*- coding: utf-8 -*-
from django.utils import timezone
from django.conf import settings
from app.logs.models import SpiderLog, UserLog
from app.video.models import BilibiliSeason


def add_spider_log(user_log_id, source, source_id, url, status, msg, response, type="fg_msg"):
    if not isinstance(type, (str,)):
        type = "fg_msg"
    logs = {
        "time": timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT),
        type: [{
            "msg": msg,
            "url": response.url,
            "data": response.body.decode("utf-8"),
            "time": timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT)
        }]}
    log = SpiderLog(user_log_id=user_log_id, source=source, source_id=source_id, url=url, status=status, logs=logs)
    log.save()
    return log


def add_user_log(type, count, discription, status="5", user_id=settings.USER_ID):
    logs = {
        "start_time": timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT),
        "discription": discription,
        "undone": discription,
        # "failed": [],
        # "success": [],
    }
    log = UserLog(user_id=user_id, log_type=type, status=status, logs=logs, count=count, success=0)
    log.save()
    return log


def add_msg(user_log, msg, response, type="fg_msg", source="spider"):
    if source == "pipeline":
        log = {
            "msg": msg,
            "url": "",
            "data": response if response else "",
            "time": timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT)
        }
        if not isinstance(type, (str,)):
            type = "fg_msg"
        if user_log.success_detail.get(type) and isinstance(user_log.success_detail[type], (tuple, list)):
            user_log.success_detail[type].append(log)
        else:
            user_log.success_detail[type] = [log, ]
    else:
        log = {
            "msg": msg,
            "url": response.url if response else "",
            "data": response.body.decode("utf-8") if response else "",
            "time": timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT)
        }
        if not isinstance(type, (str,)):
            type = "fg_msg"
        if user_log.logs.get(type) and isinstance(user_log.logs[type], (tuple, list)):
            user_log.logs[type].append(log)
        else:
            user_log.logs[type] = [log,]
    return user_log


def add_end(user_log):
    user_log.logs["end_time"] = timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT)
    return user_log


def clean_log():
    pass


def show_spider_log(user_log_id):
    pass


def update_user_log(user_log_id):
    try:
        user_log = UserLog.objects.get(id=user_log_id)
        if user_log.status == "1":
            user_log.status = "2"
        discription = user_log.logs["discription"]
        success_detail = []
        for season_id in discription:
            if find_user_log_in_season(user_log_id, season_id):
                success_detail.append(season_id)
        user_log.success = len(success_detail)
        user_log.success_detail = {"success": success_detail, "update_time": timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT)}
        if len(success_detail) == len(discription):
            user_log.success_detail["complete"] = True
        user_log.save(update_fields=['success', 'status', 'success_detail'])
    except Exception as e:
        print(e)


def find_user_log_in_season(user_log_id, season_id):
    try:
        season = BilibiliSeason.objects.get(season_id=season_id)
        for data in reversed(season.detail["details"]):
            if data.get("user_log_id") == user_log_id:
                return True
        return False
    except Exception as e:
        print(e)
