from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class SpiderLog(models.Model):
    """
    爬虫记录
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
    user_log_id = models.IntegerField()
    source = models.CharField(max_length=10, choices=SOURCE_CHOICE)
    source_id = models.IntegerField()
    url = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, db_index=True)
    logs = JSONField()  # time, proxy, response, http code, status, start time, end time,

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        pass

    def __str__(self):
        return self.url

    def add_log(self):
        pass


class UserLog(models.Model):
    """
    操作记录
    """
    STATUS_CHOICE = (
        ("0", "失败"),
        ("1", "进行中"),
        ("2", "完成"),
        ("3", "取消中"),
        ("4", "已取消"),
    )
    TYPE_CHOICE = (
        ("0", "BilibiliSeason Spider"),
    )
    user_id = models.IntegerField()
    log_type = models.CharField(max_length=10, choices=TYPE_CHOICE, db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, db_index=True)
    logs = JSONField()  # time, start, end, spend, discription

    count = models.IntegerField()
    success = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        pass

    def __str__(self):
        return self.log_type

    def add_log(self):
        pass