 # -*- coding: utf-8 -*-

import sys
import re
from django.conf import settings
from models import Article
import datetime

import urllib2
from bs4 import BeautifulSoup

"""
class Article(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'название')
    desc = RichTextField(verbose_name=u'вступительная часть')
    content = RichTextField(verbose_name=u'содержимое')
    date = models.DateField(auto_now_add=True, blank=True, verbose_name=u'дата')
    slug = models.SlugField(max_length=128, verbose_name=u'url', unique=True, blank=True, help_text=u'Заполнять не нужно')
"""        

def go():
    BASE_URL = 'http://vspomnit-vse.com/stati/'
    soup = BeautifulSoup(open('articles_old.html').read())
    Article.objects.all().delete()
    
    for a in soup.findAll('a', attrs={'class': 'blog'}):
        slug = a['href'][6:]
        name = a.findAll('h2')[0].string
        desc = a.findAll('div', attrs={'class': 'article'})[0].encode('utf-8').replace('assets/', 'static/assets/')
        
        
        print '*************'
        print slug
        print name
        print desc
        print ''
        
        
        details_url = BASE_URL + slug
        details_soup = BeautifulSoup(urllib2.urlopen(details_url).read())
        
        content = details_soup.findAll('div', attrs={'id': 'left'})[0]
        content = ''.join([str(x) for x in content.contents[2:-1]]).replace('public/', 'static/public/')
        
        Article(name=name,
                    desc=desc,
                    content=u'',
                    slug=slug).save()
        print details_url
        