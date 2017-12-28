# -*- coding: utf-8 -*-

from app.proxy.models import Proxy


def get_random_proxy(**kwargs):
    return Proxy.objects.filter(**kwargs).order_by("?").first()