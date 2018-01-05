# -*- coding: utf-8 -*-
from django.utils import timezone
from app.logs.models import SpiderLog, UserLog

def add_spider_log(user_log_id, source, source_id, url, status, msg, response, type="fg_msg"):
    if not isinstance(type, (str,)):
        type = "fg_msg"
    logs = {
        "time": timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"),
        type: [{
            "msg": msg,
            "url": response.url,
            "data": response.body,
            "time": timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        }]}
    log = SpiderLog(user_log_id=user_log_id, source=source, source_id=source_id, url=url, status=status, logs=logs)
    log.save()
    return log


def add_user_log(type, count, discription, status="5", user_id=1):
    logs = {
        "start_time": timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"),
        "discription": discription,
        "undone": discription,
    }
    log = UserLog(user_id=user_id, log_type=type, status=status, logs=logs, count=count, success=0)
    log.save()
    return log


def clean_log():
    pass


def show_spider_log(user_log_id):
    pass