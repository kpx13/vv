# -*- coding: utf-8 -*-

from django.db import models


class Subscribe(models.Model):
    name  = models.CharField(u'Имя', max_length=255)
    email  = models.CharField(u'Email', max_length=255)
    request_date = models.DateTimeField(u'дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = u'подписка'
        verbose_name_plural = u'подписки'
        ordering = ['-request_date']
    
    def __unicode__(self):
        return str(self.name)
    
    @staticmethod
    def exist(email):
        return len(Subscribe.objects.filter(email=email)) > 0

