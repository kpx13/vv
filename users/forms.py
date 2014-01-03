# -*- coding: utf-8 -*-
 
from django.forms import ModelForm, fields
from models import UserProfile, Request
 
class ProfileForm(ModelForm):
    fio = fields.CharField(required=True, label=u'ФИО *')
    email = fields.EmailField(label=u'E-mail *')
    
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