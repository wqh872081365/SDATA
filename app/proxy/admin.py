from django.contrib import admin
from app.proxy.models import *

# Register your models here.


class ProxyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Proxy, ProxyAdmin)