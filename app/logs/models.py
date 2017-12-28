from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

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

    def add_msg(self, msg, response, type="fg_msg"):
        log = {
            "msg": msg,
            "url": response.url,
            "data": response.body,
            "time": timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        }
        if not isinstance(type, (str,)):
            type = "fg_msg"
        if self.logs.get(type) and isinstance(self.logs[type], (tuple, list)):
            self.logs[type].append(log)
        else:
            self.logs[type] = [log,]


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
        ("5", "未开始"),
    )
    TYPE_CHOICE = (
        ("0", "BilibiliSeason Spider"),
    )
    user_id = models.IntegerField()
    log_type = models.CharField(max_length=10, choices=TYPE_CHOICE, db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, db_index=True)
    logs = JSONField()  # time, start, end, spend, discription(list), type, msg

    count = models.IntegerField()
    success = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        pass

    def __str__(self):
        return self.log_type

    def add_msg(self, msg, response, type="fg_msg"):
        log = {
            "msg": msg,
            "url": response.url,
            "data": response.body,
            "time": timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        }
        if not isinstance(type, (str,)):
            type = "fg_msg"
        if self.logs.get(type) and isinstance(self.logs[type], (tuple, list)):
            self.logs[type].append(log)
        else:
            self.logs[type] = [log,]

    def add_end(self):
        self.logs["end_time"] = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")