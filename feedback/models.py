# -*- coding: utf-8 -*-

from django.db import models


class Feedback(models.Model):
    name  = models.CharField(u'Имя', max_length=255)
    phone  = models.CharField(u'Телефон', blank=True, max_length=255)
    email  = models.CharField(u'Email', blank=True, max_length=255)
    skype  = models.CharField(u'Skype', blank=True, max_length=255)
    message  = models.TextField(u'Сообщение')
    request_date = models.DateTimeField(u'дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = u'заявка'
        verbose_name_plural = u'заявки'
        ordering = ['-request_date']
    
    def __unicode__(self):
        return str(self.name)

