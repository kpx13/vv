# -*- coding: utf-8 -*-

from django.db import models


class Order(models.Model):
    name  = models.CharField(u'Имя', max_length=255)
    phone  = models.CharField(u'Телефон', blank=True, max_length=255)
    email  = models.CharField(u'Email', blank=True, max_length=255)
    datetime  = models.CharField(u'Дата и время тренировки', blank=True, max_length=255)
    card  = models.CharField(u'Номер карты', blank=True, max_length=255)
    request_date = models.DateTimeField(u'дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = u'заявка'
        verbose_name_plural = u'заявки'
        ordering = ['-request_date']
    
    def __unicode__(self):
        return str(self.name)

