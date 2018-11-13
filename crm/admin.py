# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from django import forms 
from .form import Lead_statusForm

# Register your models here.

@admin.register(Usertype)
class UsertypeAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'sub_link', 'template_folder', 'use_nav_from_template_folder', 'menu_template_name', 'status',)


@admin.register(User_usertype)
class User_usertypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'usertype')


# Lead Models	
@admin.register(Leads_tbl)
class Leads_tblAdmin(admin.ModelAdmin):
	list_display = ('id','company_name', 'contact_firstname', 'contact_lastname', 'contact_details','contact_designation', 'address', 'country', 'phone', 'extension', 'fax', 'email', 'website', 'creation_date', 'last_updated')
	list_display_links = ('id', 'company_name')
	search_fields = ('company_name', 'email',)
	list_per_page = 50

@admin.register(Lead_type)	
class Lead_typeAdmin(admin.ModelAdmin):
	list_display = ('id','name', 'active')
	list_display_links = ('id', 'name')
	search_fields = ('name',)
	list_filter = ('active',)
	list_per_page = 50	

@admin.register(Lead_line_of_business)		
class Lead_line_of_businessAdmin(admin.ModelAdmin):
	list_display = ('id','name', 'active')
	list_display_links = ('id', 'name')
	search_fields = ('name',)
	list_filter = ('active',)
	list_per_page = 50	

@admin.register(Lead_payment_type)	
class Lead_payment_typeAdmin(admin.ModelAdmin):
	list_display = ('id','name', 'active')
	list_display_links = ('id', 'name')
	search_fields = ('name',)
	list_filter = ('active',)
	list_per_page = 50
	
@admin.register(Lead_probability)	   
class Lead_probabilityAdmin(admin.ModelAdmin):
	list_display = ('id','name', 'active')
	list_display_links = ('id', 'name')
	search_fields = ('name',)
	list_filter = ('active',)
	list_per_page = 50	

@admin.register(Lead_status)	
class Lead_statusAdmin(admin.ModelAdmin):
	form = Lead_statusForm
	list_display = ('id','name', 'previous_status', 'active', 'color_denoter')
	list_display_links = ('id', 'name')
	search_fields = ('name',)
	list_filter = ('active',)
	list_per_page = 50		

@admin.register(Lead_program_requirement)		
class Lead_program_requirementAdmin(admin.ModelAdmin):
	list_display = ('id','name', 'active')
	list_display_links = ('id', 'name')
	search_fields = ('name',)
	list_filter = ('active',)
	list_per_page = 50		

@admin.register(Lead_call_purpose)	
class Lead_call_purposeAdmin(admin.ModelAdmin):
	list_display = ('id','name', 'active')
	list_display_links = ('id', 'name')
	search_fields = ('name',)
	list_filter = ('active',)
	list_per_page = 50		

@admin.register(Lead_pricing_model)	
class Lead_pricing_modelAdmin(admin.ModelAdmin):
	list_display = ('id','name', 'active')
	list_display_links = ('id', 'name')
	search_fields = ('name',)
	list_filter = ('active',)
	list_per_page = 50		

@admin.register(Lead_questionnaire_model)	
class Lead_questionnaire_modelAdmin(admin.ModelAdmin):	
	list_display = ('id', 'lead_id', 'creation_date', 'last_updated')
	list_display_links = ('id', 'lead_id')
	search_fields = ('lead_id',)
	list_filter = ('creation_date',)
	list_per_page = 50	

@admin.register(User_profile)	
class User_profileAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'get_photo')
	list_per_page = 50	