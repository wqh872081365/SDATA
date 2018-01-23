# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from app.utils.rq_scheduler import add_spider_status_scheduler, list_rq_scheduler
import django_rq


class Command(BaseCommand):

    def handle(self, *args, **options):
        spider_status_scheduler = django_rq.get_scheduler("spider_status")
        spider_job = spider_status_scheduler.cron(cron_string="0 2 * * *", func=add_spider_status_scheduler, queue_name="spider_status")
        print("spider status job %s start" % (spider_job.id,))

        default_scheduler = django_rq.get_scheduler("scheduler")
        default_job = default_scheduler.cron(cron_string="0 4 * * *", func=list_rq_scheduler, queue_name="scheduler")
        print("default scheduler job %s start" % (default_job.id,))