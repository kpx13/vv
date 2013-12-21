# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'date', 'desc')
    search_fields = ('name', 'desc', 'content')

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Review, ReviewAdmin)