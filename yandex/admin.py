# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Transaction


class OrderAdmin(admin.ModelAdmin):
    list_display = ('email', 'request_date')

admin.site.register(Transaction, OrderAdmin)