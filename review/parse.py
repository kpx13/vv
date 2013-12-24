 # -*- coding: utf-8 -*-

import sys
import re
from django.conf import settings
from models import Review, Category
import datetime

import urllib2
from bs4 import BeautifulSoup

"""
class Review(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'название')
    category = models.ManyToManyField(Category, verbose_name=u'категории', related_name='articles')
    desc = RichTextField(verbose_name=u'вступительная часть')
    content = RichTextField(verbose_name=u'содержимое')
    date = models.DateField(auto_now_add=True, blank=True, verbose_name=u'дата')
    slug = models.SlugField(max_length=128, verbose_name=u'url', unique=True, blank=True, help_text=u'Заполнять не нужно')
    at_right = models.BooleanField(u'показывать в правой части', blank=True, default=True)
"""        

CATEG_AND_REVIEWS = [(1, '155'),
                     (2, '8'), 
                     (3, '16'),
                     (4, '18'),
                     (5, '21'),
                     (6, '3'),
                     (7, '46')]

def go():
    BASE_URL_AJEX = 'http://vspomnit-vse.com/ajax/otzyv'
    BASE_URL = 'http://vspomnit-vse.com/otzyivyi/'
    Review.objects.all().delete()
    for c, r in CATEG_AND_REVIEWS:
        cat = Category.objects.get(id=c)
        soup = BeautifulSoup(urllib2.urlopen(BASE_URL_AJEX + '&type=' + r).read())
        
        for a in soup.findAll('a', attrs={'class': 'otzyv'}):
            slug = a['href'][9:]
            name = a.findAll('h3')[0].string
            desc = u''.join([unicode(x) for x in a.contents[4:]]).strip()

            details_url = BASE_URL + slug
            details_soup = BeautifulSoup(urllib2.urlopen(details_url).read())
            
            content = details_soup.findAll('div', attrs={'id': 'left'})[0]
            content = ''.join([str(x) for x in content.contents[2:-1]]).replace('public/', 'static/public/')
            
            at_right = True
            if not desc:
                desc=content
                at_right = False
            
            slug = slug.replace(',', '').replace('.', '-')
            
            if Review.objects.filter(slug=slug).count() == 0:
                r = Review(name=name,
                       desc=desc,
                       content=content,
                       slug=slug,
                       at_right=at_right)
                r.save()
            else:
                r = Review.objects.get(slug=slug)
                print '!!! COPY !!!', r.id
            r.category.add(cat)
            r.save()
            
            print details_url
            
            