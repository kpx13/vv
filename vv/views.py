# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import config
from livesettings import config_value

from pages.models import Page
from review.models import Review, Category
from blog.models import BlogArticle

PAGINATION_COUNT = 10

REDIRECT_URLS = {
                    'otzyivyi': 'reviews',
                 } 

def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c['is_debug'] = settings.DEBUG
    c['recent_reviews'] = Review.objects.filter(at_right=True)[:5]
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

def blog(request, page_name=None):
    c = get_common_context(request)
    if page_name is None:
        c['title'] = u'Блог'
        items = BlogArticle.objects.all()
        
        paginator = Paginator(items, PAGINATION_COUNT)
        page = int(request.GET.get('page', '1'))
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            items = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            items = paginator.page(page)
        c['page'] = page
        c['page_range'] = paginator.page_range
        if len(c['page_range']) > 1:
            c['need_pagination'] = True
        c['items'] = items
        
        return render_to_response('blog.html', c, context_instance=RequestContext(request))
    else:
        b = BlogArticle.get_by_slug(page_name)
        c['title'] = b.name
        c['p'] = b
        return render_to_response('page.html', c, context_instance=RequestContext(request))

def services(request):
    c = get_common_context(request)
    c['title'] = u'Услуги'
    return render_to_response('services.html', c, context_instance=RequestContext(request))

def reviews(request, cat_name=None):
    c = get_common_context(request)
    if cat_name:
        category = Category.get_by_slug(cat_name)
        items = Review.objects.filter(category=category)
        c['title'] = u'Отзывы: ' + category.name
    else:
        items = Review.objects.all()
        c['title'] = u'Отзывы'
    c['categories'] = list(Category.objects.all())
    c['categories'].sort(key=lambda x: -x.count)
    c['revews_count'] = Review.objects.count()
    
    paginator = Paginator(items, PAGINATION_COUNT)
    page = int(request.GET.get('page', '1'))
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        items = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        items = paginator.page(page)
    c['page'] = page
    c['page_range'] = paginator.page_range
    if len(c['page_range']) > 1:
        c['need_pagination'] = True
    c['items'] = items
    
    return render_to_response('reviews.html', c, context_instance=RequestContext(request))

def review(request, name):
    c = get_common_context(request)
    r = Review.get_by_slug(name)
    if r:
        c.update({'p': r})
        c['title'] = r.name
        return render_to_response('page.html', c, context_instance=RequestContext(request))
    else:
        raise Http404()
