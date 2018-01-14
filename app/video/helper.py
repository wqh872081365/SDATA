# -*- coding: utf-8 -*-
from app.logs.models import UserLog

def list_spider_result():
    pass

def list_spider_failed(user_log_id, log_type):
    try:
        user_log = UserLog.objects.get(id=user_log_id, log_type=log_type)
        all_list = user_log.logs.get("discription", [])
        success_list = user_log.success_detail.get("success", [])
        failed_list = list(set(all_list) - set(success_list))
        return failed_list
    except Exception as e:
        print(e)
        return []