# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Transaction


class OrderAdmin(admin.ModelAdmin):
    list_display = ('request_date', 'message')

admin.site.register(Transaction, OrderAdmin)