# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Subscribe


class OrderAdmin(admin.ModelAdmin):
    list_display = ('request_date', 'name', 'email', )

admin.site.register(Subscribe, OrderAdmin)