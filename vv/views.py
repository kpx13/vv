# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import config
from livesettings import config_value

from pages.models import Page
from review.models import Review, Category
from blog.models import BlogArticle
from articles.models import Article
from subscribe.forms import SubscribeForm
from feedback.forms import FeedbackForm

PAGINATION_COUNT = 10
RIGHT_REVIEWS_COUNT = 3

REDIRECT_URLS = {
                    'otzyivyi': 'reviews',
                 }

SERVICES_AND_REVIEWS = {'obuchenie': 6, 
                        'regressii-v-proshlyie-zhizni': 7, 
                        #'sluzhenie': 1, 
                        'isczelenie-slavyanskogo-duxovnogo-kresta': 3, 
                        'ochishhenie-dushi': 2 } 

def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c['is_debug'] = settings.DEBUG
    c['recent_reviews'] = Review.objects.filter(at_right=True).order_by('?')[:RIGHT_REVIEWS_COUNT]
    c.update(csrf(request))
    
    form = SubscribeForm()
    if request.method == 'POST':
        if request.POST['action'] == 'subscribe':
            form = SubscribeForm(request.POST)
            if form.is_valid():
                if form.save():
                    c['form_subscribe_send'] = '1'
                else:
                    c['form_subscribe_send'] = '0'      
    c['sform'] = form
    
    return c

def page(request, page_name):
    c = get_common_context(request)
    p = Page.get_by_slug(page_name)
    if p:
        c.update({'p': p})
        c['title'] = p.title
        if page_name in SERVICES_AND_REVIEWS:
            cat = Category.objects.get(id=SERVICES_AND_REVIEWS[page_name])
            c['recent_reviews'] = Review.objects.filter(category=cat, at_right=True).order_by('?')[:RIGHT_REVIEWS_COUNT]
            c['reviews_category'] = cat
        
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

def molitva(request):
    c = get_common_context(request)
    c['title'] = u'Общая молитва'
    return render_to_response('molitva.html', c, context_instance=RequestContext(request))

def contacts(request):
    c = get_common_context(request)
    c['title'] = u'Контакты'
    c['content'] = Page.get_by_slug('contacts').content 
    
    form = FeedbackForm()
    if request.method == 'POST':
        if request.POST['action'] == 'feedback':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                form.save()
                c['form_send'] = True        
    c['form'] = form
    
    return render_to_response('contacts.html', c, context_instance=RequestContext(request))

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

def articles(request, page_name=None):
    c = get_common_context(request)
    if page_name is None:
        c['title'] = u'Статьи'
        items = Article.objects.all()
        
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
        
        return render_to_response('articles.html', c, context_instance=RequestContext(request))
    else:
        b = Article.get_by_slug(page_name)
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
        c['reviews_all'] = True
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


def conference(request):
    if request.method == 'POST':
        if request.POST['action'] == 'conference':
            c = get_common_context(request)
            c['title'] = u'Оплата доступа на конференцию'
            c['email'] = request.POST.get('email', '')
            return render_to_response('yandex.html', c, context_instance=RequestContext(request))
    else:
        c = get_common_context(request)
        c['title'] = u'Целительские сеансы онлайн'
        return render_to_response('conference.html', c, context_instance=RequestContext(request))


@csrf_exempt
def yandex(request):
    if request.method == 'POST':
        from yandex.models import Transaction
        Transaction(message=str(request.POST.dict()),
                    email=request.POST.get('label', u'!!! не заполнено')).save()
	if request.POST.get('withdraw_amount', '0') == u'500.00':
	    from django.core.mail import send_mail
	    send_mail(u'Доступ на целительский сеанс', u"А вот и ссылка: %s" % settings.CONFERENCE_LINK, [request.POST.get('label', u'mail.vspomnit.vse@gmail.com')])
	else:
	    from django.core.mail import send_mail
            send_mail(u'Доступ на целительский сеанс', u"Введённая Вами сумма не 500 руб. Если у Вас возникли проблемы пишите на mail.vspomnit.vse@gmail.com", settings.DEFAULT_FROM_EMAIL, [request.POST.get('label', u'mail.vspomnit.vse@gmail.com')])
        return HttpResponse(status=200)
    else:
        return HttpResponseRedirect('/conference/')
