# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from app.utils.rq_scheduler import list_rq_scheduler
from app.utils.scrapy import add_schedule
from app.logs.add_log import update_user_logs, count_not_finish_user_logs
from app.proxy.helper import set_vaild_proxy, set_invaild_proxy
import django_rq


class Command(BaseCommand):

    def handle(self, *args, **options):
        # spider_status
        spider_status_scheduler = django_rq.get_scheduler("spider_status")
        spider_job = spider_status_scheduler.cron(cron_string="0 2 * * *", func=update_user_logs,
                                                  queue_name="spider_status")
        print("spider status job %s start" % (spider_job.id,))

        # scheduler
        default_scheduler = django_rq.get_scheduler("scheduler")

        default_job = default_scheduler.cron(cron_string="0 4 * * *", func=list_rq_scheduler, queue_name="scheduler")
        print("default scheduler job %s start" % (default_job.id,))

        default_job_scrapyd = default_scheduler.cron(cron_string="0 5 * * *", func=count_not_finish_user_logs,
                                                     queue_name="scheduler")
        print("default scheduler job for scrapyd %s start" % (default_job_scrapyd.id,))

        # add_spider
        add_spider_scheduler = django_rq.get_scheduler("add_spider")
        args = ["wdata", "proxydb"]
        kwargs = {}
        add_spider_job = add_spider_scheduler.cron(cron_string="0 6 * * *", func=add_schedule, args=args,
                                                   kwargs=kwargs, queue_name="add_spider")
        print("add spider job %s start" % (add_spider_job.id,))

        # proxy_valid vaild
        proxy_valid_scheduler = django_rq.get_scheduler("proxy_valid")
        args = []
        kwargs = {}
        proxy_valid_job = proxy_valid_scheduler.cron(cron_string="0 7 * * *", func=set_vaild_proxy, args=args,
                                                     kwargs=kwargs, queue_name="proxy_valid")
        print("proxy valid job %s start" % (proxy_valid_job.id,))

        # proxy_valid invaild
        proxy_invalid_scheduler = django_rq.get_scheduler("proxy_valid")
        args = []
        kwargs = {}
        proxy_invalid_job = proxy_invalid_scheduler.cron(cron_string="0 0 * * 1", func=set_invaild_proxy, args=args,
                                                         kwargs=kwargs, queue_name="proxy_valid")
        print("proxy valid job %s start" % (proxy_invalid_job.id,))
