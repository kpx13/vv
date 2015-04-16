# -*- coding: utf-8 -*-

from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from ckeditor.fields import RichTextField
import pytils
from pytils import translit
import datetime
from django.db.models import Q


class QA(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'родительская категория')
    title = models.CharField(max_length=256, verbose_name=u'заголовок')
    content = RichTextField(blank=True, verbose_name=u'контент')
    slug = models.SlugField(max_length=128, verbose_name=u'слаг', unique=True, blank=True, help_text=u'Заполнять не нужно')
    order = models.IntegerField(null=True, blank=True, default=0, verbose_name=u'порядок сортировки', help_text=u'Заполнять не обязательно')    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.title)
        super(QA, self).save(*args, **kwargs)
        if self.order == 0:
            self.order = self.id
            self.save()
    
    @staticmethod
    def get_by_slug(page_name):
        try:
            return QA.objects.get(slug=page_name)
        except:
            return None
        
    class Meta:
        verbose_name = u'позиция'
        verbose_name_plural = u'вопросы-ответы'

    class MPTTMeta:
        order_insertion_by = ['title']
        
    def __unicode__(self):
        return '%s%s' % (' -- ' * self.level, self.title)
    
    @staticmethod
    def get(id_):
        try:
            return QA.objects.get(id=id_)
        except:
            return None
