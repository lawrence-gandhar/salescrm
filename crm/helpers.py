# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# IntegrityError Exception for checking duplicate entry, 
# connection import to establish connection to database 
from django.db import IntegrityError, connection 

# Django settings from settings.py
from django.conf import settings	

# Condition operators for models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from .models import Usertype, User_usertype

from crm.models.users import User_usertype, Usertype
from crm.models.leads import Leads_tbl, Lead_type, Lead_line_of_business, Lead_payment_type, Lead_probability
from crm.models.leads import Lead_status, Lead_program_requirement, Lead_call_purpose, Lead_pricing_model, Lead_questionnaire_model

# system related imports
import sys, os, csv, json, datetime, random, string


# CURRENT USERTYPE SUBLINK
#
def current_user_url(value):
    value = int(value)
    url_link = ''

    try:
        usertype = User_usertype.objects.get(user_id = value)
        usertype_id = usertype.usertype_id

        try:
            target_link = Usertype.objects.get(pk = int(usertype_id))
            url_link = target_link.sub_link

        except User_usertype.DoesNotExist:
            pass 
        except TypeError: 
            pass       

    except User_usertype.DoesNotExist:
        pass    
    except TypeError: 
        pass

    return url_link


#
# LEADS FORM ELEMENTS
#

#
# DROPDOWNS
#

def dropdowns(data = (),selected = 0):
    
    html = ['<option value="0">-- Select --</option>']

    if selected == 0:
        html = ['<option value="0" selected>-- Select --</option>']

    for row in data:

        html.append('<option value="'+str(row["id"])+'"')
        if row["id"] == selected:
            html.append(' selected ')
        html.append('>'+row["name"]+'</option>')

    return ''.join(html)

#
# CHECKBOXES
#
def checkboxes(data = (),selected = [], name = ""):

    html_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    html = []

    i = 0
    for row in data:
        html.append('<div class="checkbox checkbox-primary col-md-4">')
        html.append('<input id="'+html_id+str(i)+'" class="styled" type="checkbox" value="'+str(row["id"])+'" name = "'+name+'"')

        print(selected)

        if str(row["id"]) in selected: 
            html.append(' checked')

        html.append('><label for="'+html_id+str(i)+'">'+row["name"]+'</label></div>')    
        i +=1
    return ''.join(html)    

#
# RADIOS 
#

def radios(data = (), selected = 0, name = ""):

    html = []
    i = 0
    for row in data:
        html.append('<div class="radio radio-success">')
        html.append('<input type="radio" id="singleRadio'+str(i)+'" value="'+str(row["id"])+'" name = "'+name+'"')
        
        if row["id"] == selected:
            html.append(' checked ')
        html.append('><label></label></div>')
        i += 1
    return ''.join(html)  


#
# CALLER FUNCTIONS
#

def lead_type(selected = 0):
    return dropdowns(Lead_type.objects.filter(active = True).values('id', 'name'), selected)

def lead_line_of_business(selected = 0, name = ""):
    return dropdowns(Lead_line_of_business.objects.filter(active = True).values('id', 'name'), selected)

def lead_payment_type(selected = 0, name = ""):
    return dropdowns(Lead_payment_type.objects.filter(active = True).values('id', 'name'), selected)

def lead_probability(selected = 0, name = ""):
    return dropdowns(Lead_probability.objects.filter(active = True).values('id', 'name'), selected)

def lead_program_requirement(selected = [], name = ""):
    return checkboxes(Lead_program_requirement.objects.filter(active = True).values('id', 'name'), selected, name) 

def lead_call_purpose(selected = [], name = ""):
    return checkboxes(Lead_call_purpose.objects.filter(active = True).values('id', 'name'), selected, name) 

def lead_pricing_model(selected = [], name = ""):
    return checkboxes(Lead_pricing_model.objects.filter(active = True).values('id', 'name'), selected, name) 


#
#   COUNTRY LIST DROPDOWN
#     

def country_list(selected = []):

    html = ['<option value="">-- Select Country --</option>']
    with open(settings.BASE_DIR+"/crm/static/uploads/country_list.json") as json_file:  
        data = json.load(json_file)

        for country in data:
            html.append('<option value="'+country["code"]+'"')
            if country["code"] in selected:
                html.append(' selected ')
            html.append('>'+country["name"]+'</option>')

    return ''.join(html)    

def country_json():
    with open(settings.BASE_DIR+"/crm/static/uploads/country_list.json") as json_file:  
        return json.load(json_file)   
