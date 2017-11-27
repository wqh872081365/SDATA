from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class SpiderLog(models.Model):
    """
    爬虫异常
    """
    SOURCE_CHOICE = (
        ("0", "BilibiliSeason"),
    )
    STATUS_CHOICE = (
        ("-1", "url不存在"),
        ("0", "爬取失败"),
        ("1", "存储成功"),
        ("2", "数据异常"),
        ("3", "字段异常"),
        ("4", "other"),
    )
    source = models.CharField(max_length=10, choices=SOURCE_CHOICE)
    source_id = models.IntegerField()
    url = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, db_index=True)
    logs = JSONField()  # time, proxy, response, http code, status

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("source", "source_id")

    def __str__(self):
        return self.url

    def add_log(self):
        pass