# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    
    #url(r'^accounts/', include('registration.urls'), {'extra_context': { 'title': u'Восстановление пароля'}}),
    url(r'^register/$' , views.register),
    url(r'^logout/$' , views.logout_user),
    url(r'^cabinet/$' , views.lk),
                       
    url(r'^$', views.home),
    url(r'^(?P<cat_name>[\w-]+)/$', views.home),
    url(r'^(?P<cat_name>[\w-]+)/(?P<sec_name>[\w-]+)/$', views.home),
    
)
