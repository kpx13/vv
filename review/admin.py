# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_dat', 'slug', 'id')
    search_fields = ('name',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'date', 'desc', 'at_right')
    search_fields = ('name', 'desc', 'content')
    list_filter = ('category',)

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Review, ReviewAdmin)
