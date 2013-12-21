# -*- coding: utf-8 -*-
from django.db import models

class Subscribe(models.Model):
    email  = models.CharField(u'Email', max_length=255)
    request_date = models.DateTimeField(u'дата заявки', auto_now_add=True)
                    
    class Meta:
        verbose_name = u'подписка'
        verbose_name_plural = u'подписки'
        ordering = ['-request_date']

    def __unicode__(self):
        return self.email
