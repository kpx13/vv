# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Category, Section


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)

class SectionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'slug', 'order')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Section, SectionAdmin)