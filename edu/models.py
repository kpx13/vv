# -*- coding: utf-8 -*-

from django.db import models
from ckeditor.fields import RichTextField
import pytils


class Category(models.Model):
    name  = models.CharField(u'название', max_length=255)
    slug = models.SlugField(max_length=128, verbose_name=u'url', unique=True, blank=True, help_text=u'Заполнять не нужно')
    right_content = RichTextField(blank=True, verbose_name=u'контент справа')
    content = RichTextField(blank=True, verbose_name=u'общая информация', help_text=u'Когда у юзера нет доступа')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    @staticmethod
    def get_by_slug(slug):
        try:
            return Category.objects.get(slug=slug)
        except:
            return None
    
    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'категории'
        ordering = ['id']
    
    def __unicode__(self):
        return self.name
    
class Section(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'категория', related_name='section')
    name  = models.CharField(u'название', max_length=255)
    slug = models.SlugField(max_length=128, verbose_name=u'url', blank=True, help_text=u'Заполнять не нужно')
    order = models.IntegerField(blank=True, null=True, verbose_name=u'порядковый номер')
    content = RichTextField(blank=True, verbose_name=u'контент')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name)
        super(Section, self).save(*args, **kwargs)
        if not self.order:
            self.order=self.id
            self.save()
    
    @staticmethod
    def get_by_slug(cat, sec_slug):
        try:
            return Section.objects.get(category=cat, slug=sec_slug)
        except:
            return None
    
    class Meta:
        verbose_name = u'раздел в категории'
        verbose_name_plural = u'разделы в категориях'
        ordering = ['order']
    
    def __unicode__(self):
        return u'%s - %s' % (self.category.name, self.name)
