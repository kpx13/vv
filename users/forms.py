# -*- coding: utf-8 -*-
 
from django.forms import ModelForm, fields
from models import UserProfile, Request
 
class ProfileForm(ModelForm):
    fio = fields.CharField(required=True, label=u'ФИО *', help_text=u'(Полностью!)')
    email = fields.EmailField(label=u'E-mail *')
    photo = fields.FileField(required=True, label=u'Фото *', help_text=u'(Файл не более 1Мб)')
    
    class Meta:
        model = UserProfile
        fields = ('fio', 'email', 'skype', 'vk', 'photo', 'about')
    
    
class ProfileLKForm(ModelForm):   
    class Meta:
        model = UserProfile
        fields = ('skype', 'vk', 'about')
        
        
class RequestForm(ModelForm):   
    class Meta:
        model = Request
        fields = ('comment', )
