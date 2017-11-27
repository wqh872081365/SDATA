from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Proxy(models.Model):
    """
    代理
    """
    STATUS_CHOICE = (
        ("0", "失效"),
        ("1", "异常"),
        ("2", "有效"),
    )
    ip = models.CharField(max_length=255)
    port = models.IntegerField()
    source = models.CharField(max_length=255)
    anonymity = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    https = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_CHOICE)

    detail = JSONField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        pass

    def __str__(self):
        return self.url