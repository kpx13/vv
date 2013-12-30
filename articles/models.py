# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
import pytils

class Article(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'название')
    desc = RichTextField(verbose_name=u'вступительная часть')
    content = RichTextField(verbose_name=u'содержимое')
    date = models.DateField(auto_now_add=True, blank=True, verbose_name=u'дата')
    slug = models.SlugField(max_length=128, verbose_name=u'url', unique=True, blank=True, help_text=u'Заполнять не нужно')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name)
        super(Article, self).save(*args, **kwargs)
    
    @staticmethod
    def get_by_slug(slug):
        try:
            return Article.objects.get(slug=slug)
        except:
            return None
    
    class Meta:
        verbose_name = u'статья'
        verbose_name_plural = u'статьи'
        ordering = ['-date']
        
    
    def __unicode__(self):
        return self.name
    