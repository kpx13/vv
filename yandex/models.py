# -*- coding: utf-8 -*-

from django.db import models


class Transaction(models.Model):
    message  = models.TextField(u'Запрос')
    request_date = models.DateTimeField(u'дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = u'транзакция'
        verbose_name_plural = u'транзакции'
        ordering = ['-request_date']
    
    def __unicode__(self):
        return str(self.name)

