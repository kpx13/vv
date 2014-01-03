# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.conf import settings
from django.core.context_processors import csrf
from django.forms.util import ErrorList
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.http import urlquote
import string
import random

from models import Category, Section
from users.forms import ProfileForm, ProfileLKForm, RequestForm

def password_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c['is_debug'] = settings.DEBUG
    c['user'] = request.user
    c['title'] = u'Обучение'
    c.update(csrf(request))
    return c

def home(request, cat_name=None, sec_name=None):
    c = get_common_context(request)
    
    if not request.user.is_authenticated():
        if cat_name is None:
            category = Category.get_by_slug('first')
        else:        
            category = Category.get_by_slug(cat_name)
        
        if sec_name is None:
            section = Section.objects.filter(category=category)[0]
        else:
            section = Section.get_by_slug(category, sec_name)
        
        c['title'] = u''
        c['can_request'] = (category.id == 1)
        c['category'] = category
        c['section'] = section
        c['request_url'] = '/'.join(['edu', category.slug, section.slug])
        return render_to_response('section_deny.html', c, context_instance=RequestContext(request))
    
    user = request.user
    profile = user.get_profile()
    have_access = list(profile.have_access())
    
    if cat_name is None:
        if len(have_access) > 0:
            category = have_access[-1]
        else:
            category = Category.get_by_slug('first')
    else:        
        category = Category.get_by_slug(cat_name)
        
    can_access = category in have_access
    
    request_form = RequestForm()
    if request.method == "POST":
        if request.POST['action'] == 'request':
            request_form = RequestForm(request.POST)
            if request_form.is_valid():
                r = request_form.save(commit=False)
                r.profile = profile
                r.category = category
                r.save()
                r.send()
                return HttpResponseRedirect(request.path)
    c['request_form'] = request_form
    
    if sec_name is None:
        section = Section.objects.filter(category=category)[0]
        if 'section' in request.session:
            sections = Section.objects.filter(category=category, id=request.session['section'])
            if sections:
                section = sections[0]
    else:
        section = Section.get_by_slug(category, sec_name)
        request.session['section'] = section.id
        
    c['category'] = category
    c['section'] = section
    c['request_url'] = '/'.join(['edu', category.slug, section.slug])
    if can_access:
        c['title'] = section.name
        return render_to_response('section_allow.html', c, context_instance=RequestContext(request))
    else:
        c['title'] = u''
        c['can_request'] = (category.id == 1) or (category.id == (len(have_access) + 1))
        c['status'] = profile.status(category)
        return render_to_response('section_deny.html', c, context_instance=RequestContext(request))


def register(request):
    c = get_common_context(request)
    register_form = ProfileForm()
    c['register_form'] = register_form
    auth_form = AuthenticationForm()
    c['auth_form'] = auth_form
    
    if request.method == "POST":
        if request.POST['action'] == 'register':
            register_form = ProfileForm(request.POST, request.FILES)
            if register_form.is_valid():
                error = False
                if len(User.objects.filter(username=register_form.data.get('email'))):
                    register_form._errors["email"] = ErrorList([u'Такой емейл уже зарегистрирован.'])
                    error = True
                if not error:
                    email = register_form.data.get('email')
                    u = User(username= email, 
                             email=email,
                             first_name=register_form.data.get('fio'))
                    password = password_generator()
                    u.set_password(password)
                    u.save()
                    p = register_form.save(commit=False)
                    p.user = u
                    p.save()
                    user = auth.authenticate(username=email, password=password)
                    auth.login(request, user)
                    
                    p.send(password)
                    
                    return HttpResponseRedirect('/edu/')
            c['register_form'] = register_form
        elif request.POST['action'] == 'auth':
            auth_form = AuthenticationForm(request.POST)
            if auth_form.is_valid():
                pass
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/edu/')
            else:
                auth_form._errors = {}
                auth_form._errors["username"] = ErrorList([u'Неверный логин или пароль.'])
            c['auth_form'] = auth_form
    
    c['title'] = u'Регистрация'
    
    return render_to_response('register.html', c, context_instance=RequestContext(request))

def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def lk(request):
    c = get_common_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    user_profile = request.user.get_profile()
    c['form'] = ProfileLKForm(instance=user_profile)
    c['passform'] = PasswordChangeForm(request.user)
    
    if request.method == 'POST':
        if request.POST.get('action', '') == 'data':
            form = ProfileLKForm(request.POST, instance=user_profile)
            u = request.user
            if form.is_valid():
                form.save()
            c['form'] = form
        if request.POST.get('action', '') == 'password':
            passform = PasswordChangeForm(request.user, request.POST)
            if passform.is_valid():
                passform.save()
                messages.success(request, u'Вы успешно сменили пароль.')
                return HttpResponseRedirect('/edu/cabinet/')
            else:
                c['passform'] = passform
    c['title'] = u'Личный кабинет'
    
    return render_to_response('lk.html', c, context_instance=RequestContext(request))