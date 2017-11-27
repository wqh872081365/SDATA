from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class SpiderLog(models.Model):
    """
    爬虫异常
    """
    SOURCE_CHOICE = (
        ("bilibili_season", "BilibiliSeason"),
    )
    STATUS_CHOICE = (
        ("0", "爬取失败"),
        ("1", "json异常"),
        ("2", "字段异常"),
        ("3", "存储成功"),
    )
    source = models.CharField(max_length=255, choices=SOURCE_CHOICE)
    url = models.CharField(max_length=255)
    proxy_host = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_CHOICE)
    times = models.IntegerField()
    logs = JSONField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        pass

    def __str__(self):
        return self.url

    def add_log(self):
        pass