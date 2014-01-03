# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from models import UserProfile, Request

class UserProfileInline(admin.StackedInline): 
    model = UserProfile
    extra = 0

class ExtUserAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]
    list_display = UserAdmin.list_display + ('is_active',)

class RequestAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'approved', 'date_request', 'date_approve', 'comment')

admin.site.unregister(User)
admin.site.register(User, ExtUserAdmin)
admin.site.register(Request, RequestAdmin)