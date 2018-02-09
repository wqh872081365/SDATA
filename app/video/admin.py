from django.contrib import admin
from app.video.models import *

# Register your models here.


class BilibiliSeasonAdmin(admin.ModelAdmin):
    pass


admin.site.register(BilibiliSeason, BilibiliSeasonAdmin)
