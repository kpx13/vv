 # -*- coding: utf-8 -*-

import sys
import re
from django.conf import settings
from models import BlogArticle
import datetime

import urllib2
from bs4 import BeautifulSoup

"""
class BlogArticle(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'название')
    desc = RichTextField(verbose_name=u'вступительная часть')
    content = RichTextField(verbose_name=u'содержимое')
    date = models.DateField(auto_now_add=True, blank=True, verbose_name=u'дата')
    slug = models.SlugField(max_length=128, verbose_name=u'url', unique=True, blank=True, help_text=u'Заполнять не нужно')
"""        

def go(filename='templates/blog_old.html'):
    f = open(filename, 'r')
    soup = BeautifulSoup(f.read())
    BASE_URL = 'http://vspomnit-vse.com/blog/'
    for a in soup.findAll('a', attrs={'class': 'blog'}):
        slug = a['href'][5:]
        name = a.findAll('h2')[0].string
        desc = a.findAll('div', attrs={'class': 'blog-content'})[0]
        desc = ''.join([str(x) for x in desc.contents[1:-1]])
        date_d, date_m, date_y = a.contents[0].strip().split(' / ')
        date = datetime.date(day=int(date_d), month=int(date_m), year=int(date_y))
        
        details_url = BASE_URL + slug
        details_soup = BeautifulSoup(urllib2.urlopen(details_url).read())
        
        content = details_soup.findAll('div', attrs={'id': 'left'})[0]
        content = ''.join([str(x) for x in content.contents[2:-1]]).replace('public/', 'static/public/')
        
        BlogArticle(name=name,
                    desc=desc,
                    content=content,
                    date=date,
                    slug=slug).save()
        print details_url
    
    f.close()