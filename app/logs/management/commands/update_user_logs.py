# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from app.logs.add_log import update_user_logs


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('user_log_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for user_log_id in options['user_log_id']:
            update_user_logs(user_log_id)
            print("user_log_id %s ok" % (user_log_id,))