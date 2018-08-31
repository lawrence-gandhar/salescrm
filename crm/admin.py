# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from django import forms 

# Register your models here.

@admin.register(Usertype)
class UsertypeAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'sub_link', 'template_folder', 'use_nav_from_template_folder', 'menu_template_name', 'status',)


@admin.register(User_usertype)
class User_usertypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'usertype')


