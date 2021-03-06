# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

import settings
import views

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),
    
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url(r'^settings/', include('livesettings.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),

    url(r'^edu/', include('edu.urls')),

    url(r'^$', views.pre),
    url(r'^home/$', views.home),
    url(r'^molitva/$', views.molitva),
    url(r'^contacts/$', views.contacts),
    url(r'^blog/(?P<page_name>[\w-]+)/$', views.blog),
    url(r'^blog/$', views.blog),
    url(r'^article/(?P<page_name>[\w-]+)/$', views.articles),
    url(r'^articles/$', views.articles),
    url(r'^stati/(?P<page_name>[\w-]+)/$', views.articles),
    url(r'^stati/$', views.articles),
    url(r'^reviews/(?P<cat_name>[\w-]+)/$', views.reviews),
    url(r'^reviews/$', views.reviews),
    url(r'^review/(?P<name>[\w-]+)/$', views.review),
    url(r'^otzyivyi/(?P<name>[\w-]+)/$', views.review),
    url(r'^otzyivyi/$', views.reviews),
    
    url(r'^conference/$', views.conference),
    url(r'^yandex/$', views.yandex),
    url(r'^qa/$', views.qa),
    
    url(r'^services/$', views.services),
    url(r'^uslugi/$', views.services),
    url(r'^uslugi/(?P<page_name>[\w-]+)/$', views.page),
    url(r'^(?P<page_name>[\w-]+)/$' , views.page),
)
