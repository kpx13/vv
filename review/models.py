# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
import pytils

class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'название')
    slug = models.SlugField(max_length=128, verbose_name=u'url', unique=True, blank=True, help_text=u'Заполнять не нужно')
    
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
    
    @property
    def count(self):
        return Review.objects.filter(category=self).count()
    
    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'категории'
        
    def __unicode__(self):
        return self.name

class Review(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'название')
    category = models.ManyToManyField(Category, verbose_name=u'категории', related_name='articles')
    desc = RichTextField(verbose_name=u'вступительная часть')
    content = RichTextField(verbose_name=u'содержимое')
    date = models.DateField(auto_now_add=True, blank=True, verbose_name=u'дата')
    slug = models.SlugField(max_length=128, verbose_name=u'url', unique=True, blank=True, help_text=u'Заполнять не нужно')
    at_right = models.BooleanField(u'показывать в правой части', blank=True, default=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name)
        super(Review, self).save(*args, **kwargs)
    
    @staticmethod
    def get_by_slug(slug):
        try:
            return Review.objects.get(slug=slug)
        except:
            return None
    
    class Meta:
        verbose_name = u'отзыв'
        verbose_name_plural = u'отзывы'
    
    def __unicode__(self):
        return self.name
    