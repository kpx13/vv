# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
 

from pages.models import Page
from review.models import Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import config
from livesettings import config_value
from django.conf import settings

PAGINATION_COUNT = 5

REDIRECT_URLS = {
                    'otzyivyi': 'reviews',
                    'uslugi/obuchenie': 'obuchenie',
                    'uslugi/ochishhenie-dushi': 'ochishhenie-dushi',
                 } 

def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c['is_debug'] = settings.DEBUG
    c['recent_reviews'] = Review.objects.all()[:5]
    c.update(csrf(request))
    return c

def page(request, page_name):
    c = get_common_context(request)
    p = Page.get_by_slug(page_name)
    if p:
        c.update({'p': p})
        c['title'] = p.title
        return render_to_response('page.html', c, context_instance=RequestContext(request))
    else:
        if page_name in REDIRECT_URLS:
            return HttpResponseRedirect('/' + REDIRECT_URLS[page_name] + '/')
        raise Http404()

def home(request):
    c = get_common_context(request)
    c['request_url'] = 'home'
    c['title'] = u'Главная'
    return render_to_response('home.html', c, context_instance=RequestContext(request))

def services(request):
    c = get_common_context(request)
    c['title'] = u'Услуги'
    return render_to_response('services.html', c, context_instance=RequestContext(request))

def reviews(request):
    c = get_common_context(request)
    c['reviews_all'] = Review.objects.all()
    c['title'] = u'Отзывы'
    return render_to_response('reviews.html', c, context_instance=RequestContext(request))
