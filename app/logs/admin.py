from django.contrib import admin
from app.logs.models import *

# Register your models here.


class SpiderLogAdmin(admin.ModelAdmin):
    pass


class UserLogAdmin(admin.ModelAdmin):
    pass


admin.site.register(SpiderLog, SpiderLogAdmin)
admin.site.register(UserLog, UserLogAdmin)