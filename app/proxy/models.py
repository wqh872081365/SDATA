from django.db import models
from django.contrib.postgres.fields import JSONField

import datetime

# Create your models here.


class Proxy(models.Model):
    """
    代理
    """
    STATUS_CHOICE = (
        ("0", "失效"),
        ("1", "有效"),
        ("2", "异常"),
    )
    ANONYMITY_CHOICE = (
        ("-1", "unknown"),
        ("0", "透明"),
        ("1", "匿名"),
        ("2", "高匿"),
    )
    HTTP_CHOICE = (
        ("-1", "unknown"),
        ("0", "http"),
        ("1", "https"),
        ("2", "socks4"),
        ("3", "socks5"),
    )
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    source = models.TextField()
    anonymity = models.CharField(max_length=10, choices=ANONYMITY_CHOICE, db_index=True)
    country = models.CharField(max_length=100)
    http = models.CharField(max_length=10, choices=HTTP_CHOICE, db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, db_index=True)

    detail = JSONField()  # time, detail, source

    success_count = models.IntegerField()
    failure_count = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("ip", "port")

    def __str__(self):
        return "%s:%s" % (self.ip, self.port)

    def clean_old(self):
        pass