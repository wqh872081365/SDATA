from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class BilibiliSeason(models.Model):
    """
    b站番剧
    """
    season_id = models.IntegerField(unique=True)
    season_name = models.CharField(max_length=255)
    bangumi_id = models.IntegerField(db_index=True)
    bangumi_name = models.CharField(max_length=255)

    season_url = models.URLField()
    play_count = models.BigIntegerField()
    detail = JSONField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        pass

    def __str__(self):
        return "%s%s" % (self.bangumi_name, self.season_name)