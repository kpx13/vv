# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, Template
import config
from livesettings import config_value

import pytils
import datetime

from edu.models import Category

def sendmail(subject, body, to_email):
    mail_subject = ''.join(subject)
    send_mail(mail_subject, body, settings.DEFAULT_FROM_EMAIL,
        [to_email])

class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profile', verbose_name=u'пользователь')
    fio = models.CharField(max_length=256, blank=True, verbose_name=u'ФИО')
    skype = models.CharField(max_length=256, blank=True, verbose_name=u'skype')
    vk = models.CharField(max_length=256, blank=True, verbose_name=u'vk')
    photo = models.ImageField(upload_to=lambda instance, filename: 'uploads/edu/' + pytils.translit.translify(filename),
                              max_length=256, blank=True, verbose_name=u'фото')
    about = models.TextField(blank=True, verbose_name=u'о себе')
    requests = models.ManyToManyField(Category, through='Request')
    
    def have_access(self):
        return [x.category for x in Request.objects.filter(profile=self, approved=True).order_by('id')]
    
    def status(self, category):
        requests = Request.objects.filter(profile=self, category=category)
        if len(requests) == 0:
            #return u'Вы не подавали заявку на данный курс'
            return ''
        r = requests[0]
        if r.approved:
            return u'Вы имеете доступ к данному курсу.'
        d = r.date_request
        return u'Ваша заявка была отправлена. Ожидайте подтверждения на e-mail.'
        

    class Meta:
        verbose_name = u'профиль пользователя'
        verbose_name_plural = u'профили пользователей'
    
    def __unicode__ (self):
        return str(self.user.username)

    def send(self, password):
        subject=u'Вы успешно зарегистрировались на сайте vspomnit-vse.com.',
        body_templ=u"""
ФИО: {{ profile.fio }}
E-mail: {{ profile.user.email }}
Skype: {{ profile.skype }}
VK: {{ profile.vk }}
О себе: {{ profile.about }}

Данные для входа:
E-mail: {{ profile.user.email }}
Пароль: {{ password }} (Пароль Вы можете поменять в личном кабинете на сайте.)

Вход в раздел Обучение: {{ site }}/edu/register/
"""
        body = Template(body_templ).render(Context({'profile': self, 
                                                    'password': password,
                                                    'site': 'http://vspomnit-vse.com'}))
        sendmail(subject, body, self.user.email)
        

class Request(models.Model):
    profile = models.ForeignKey(UserProfile)
    category = models.ForeignKey(Category)
    comment = models.TextField(verbose_name=u'комментарий')
    approved = models.BooleanField(default=False, verbose_name=u'одобрено')
    date_request = models.DateTimeField(blank=True, default=datetime.datetime.now(), verbose_name='дата заявки')
    date_approve = models.DateTimeField(blank=True, null=True, default=None, verbose_name='дата отодбрения')
    
    class Meta:
        verbose_name = u'запрос'
        verbose_name_plural = u'запросы'
    
    def __unicode__ (self):
        return '%s - %s' % (self.profile.user.first_name, self.category.name)
    
    def save(self, *args, **kwargs):
        if self.approved:
            subject=u'Ваша заявка на %s была одобрена.' % self.category.name ,
            body_templ=u"""
    {{ profile.fio }}, Ваша заявка была одобрена.
    
    Заказана услуга: {{ category.name }}
    Дата: {{ request.date_request }}
    Комментарий: {{ request.comment }}
    
    Вы можете получить доступ к материалам по адресу: {{ site }}/edu/
    Войдите под своим логином и паролем. Если Вы забыли пароль, напишите администации по адресу admin@vspomnit-vse.com.
    
    
    """
            body = Template(body_templ).render(Context({'profile': self.profile, 
                                                        'category': self.category,
                                                        'request': self, 
                                                        'site': 'http://vspomnit-vse.com'}))
            sendmail(subject, body, self.profile.user.email)
            
        super(Request, self).save(*args, **kwargs)
    
    def send(self):
        subject=u'Поступила новая заявка на обучение (%s).' % self.category.name ,
        body_templ=u"""
ФИО: {{ profile.fio }}
E-mail: {{ profile.user.email }}
Skype: {{ profile.skype }}
VK: {{ profile.vk }}
Фоточка: {{ site }}/media/{{ profile.photo }}
О себе: {{ profile.about }}

Заказана услуга: {{ category.name }}
Дата: {{ request.date_request }}
Комментарий: {{ request.comment }}

Ссылка на заказ: {{ site }}/admin/users/request/{{ request.id }}/
"""
        body = Template(body_templ).render(Context({'profile': self.profile, 
                                                    'category': self.category,
                                                    'request': self, 
                                                    'site': 'http://vspomnit-vse.com'}))
        sendmail(subject, body, config_value('MyApp', 'EMAIL'))
        