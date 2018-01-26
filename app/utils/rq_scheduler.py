# -*- coding: utf-8 -*-
import django_rq
from django.utils import timezone
from app.utils.scrapy import list_projects, list_jobs
from app.logs.models import UserLog
from app.logs.add_log import update_user_log

SCHEDULER_LIST = ["scheduler", "spider_status", "rq_worker_number_control", "proxy_valid"]


def list_rq_scheduler(until=None):
    if until:
        if isinstance(until, (timezone.datetime, timezone.timedelta)):
            kwargs = {"until": until}
        else:
            kwargs = {}
            print("until is not valid")
    else:
        kwargs = {}
    for scheduler_name in SCHEDULER_LIST:
        scheduler = django_rq.get_scheduler(scheduler_name)
        list_of_job_instances = scheduler.get_jobs(with_times=True, **kwargs)
        print("scheduler_name: ", list_of_job_instances)


def scheduler_cancel(scheduler_name, job_id):
    scheduler = django_rq.get_scheduler(scheduler_name)
    if job_id in scheduler:
        scheduler.cancel(job_id)
        print(scheduler_name, job_id, "cannel ok")
    else:
        print("%s not find in %s" % (job_id, scheduler_name))