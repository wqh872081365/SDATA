# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings

from app.video.models import BilibiliSeason
from app.logs.models import UserLog

import pytz


# class Command(BaseCommand):
#
#     def add_arguments(self, parser):
#         parser.add_argument('user_log_id', nargs='+', type=int)
#
#     def handle(self, *args, **options):
#         for user_log_id in options['user_log_id']:
#             try:
#                 user_log = UserLog.objects.get(id=user_log_id)
#                 start_time = user_log.logs.get("start_time", "")
#                 end_time = user_log.logs.get("end_time", "")
#                 result_list = user_log.logs.get("discription", [])
#                 if start_time and end_time:
#                     start_time = timezone.datetime.strptime(start_time, settings.LOG_DATE_FORMAT).replace(tzinfo=pytz.UTC)
#                     end_time = timezone.datetime.strptime(end_time, settings.LOG_DATE_FORMAT).replace(tzinfo=pytz.UTC)
#                     failed_list = []
#                     for result in result_list:
#                         if not self.get_result(result, start_time, end_time):
#                             print("%s not find detail in time" % (user_log_id,))
#                             failed_list.append(result)
#                     print("result list count %s, not find count %s" % (len(result_list), len(failed_list)))
#                     print("failed list %s" % (failed_list,))
#                 else:
#                     print("not find start time or end time for %s" % (user_log_id,))
#             except Exception as e:
#                 print("not find user_log %s" % (user_log_id,))
#
#     def get_result(self, season_id, start_time, end_time):
#         season = BilibiliSeason.objects.get(season_id)
#         if season.detail.get("details", []) and isinstance(season.detail["details"], (list, tuple)):
#             time = season.detail["details"][-1].get("time", "")
#             if time:
#                 time = timezone.datetime.strptime(time, settings.LOG_DATE_FORMAT).replace(tzinfo=pytz.UTC)
#                 if time > start_time and time < end_time:
#                     return True
#         return False