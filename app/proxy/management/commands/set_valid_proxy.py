# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from app.proxy.helper import set_vaild_proxy


class Command(BaseCommand):

    def handle(self, *args, **options):
        set_vaild_proxy()
