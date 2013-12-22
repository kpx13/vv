# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'date', 'desc',)
    search_fields = ('name', 'desc', 'content')

admin.site.register(models.Article, ArticleAdmin)