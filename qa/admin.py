# -*- coding: utf-8 -*-
from django.contrib import admin
from models import QA
 
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'parent', 'order')

admin.site.register(QA, CategoryAdmin)
