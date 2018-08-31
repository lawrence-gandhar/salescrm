# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# IntegrityError Exception for checking duplicate entry, 
# connection import to establish connection to database 
from django.db import IntegrityError, connection 

# Used for serializing object data to json string
from django.core.serializers.json import DjangoJSONEncoder 
from django.core.serializers import serialize

from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect

# Paginator class import
from django.core.paginator import Paginator

# Django settings from settings.py
from django.conf import settings	

# Condition operators for models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# Other imports
from django.shortcuts import render, redirect

from .models import Usertype, User_usertype
#from .models import Assessment_Settings, AssessmentFormOptions, AssessmentFormQuestions, AssessmentFormSection

import sys, os, csv, json, datetime

#
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#
from django.contrib import messages

# Create your views here.

#*******************************************************************************
# AUTHENTICATION  
#*******************************************************************************   

def index(request):
    submit = request.POST.get("submit", False)

    if submit:
        
        user = authenticate(username = request.POST["username"], password = request.POST["password"])
        
        if user is not None:
            
            login(request, user)

            url_link = '/'

            try:
                usertype = User_usertype.objects.get(user_id = int(user.id))
                usertype_id = usertype.usertype_id

                try:
                    target_link = Usertype.objects.get(pk = int(usertype_id))
                    url_link = target_link.sub_link

                except User_usertype.DoesNotExist:
                    messages.error(request, 'Error occurred during authentication.<br/> Please Contact Administrator')
                    return redirect('/', 'refresh')      
                except TypeError: 
                    messages.error(request, 'Error occurred during authentication.<br/> Please Contact Administrator')
                    return redirect('/', 'refresh')           

            except User_usertype.DoesNotExist:
                messages.error(request, 'Error occurred during authentication.<br/> Please Contact Administrator')
                return redirect('/', 'refresh')      
            except TypeError: 
                messages.error(request, 'Error occurred during authentication.<br/> Please Contact Administrator')
                return redirect('/', 'refresh')      

            return redirect(url_link + '/dashboard/')
        messages.error(request, 'Invalid Username or Password')
    return render(request, 'crm/login.html', {})


#*******************************************************************************
# LOGOUT  
#*******************************************************************************   

@login_required
def user_logout(request, usertype = None):
    logout(request)
    return HttpResponseRedirect('/')   


#*******************************************************************************
# PASSWORD CHANGE
#*******************************************************************************    

@login_required
def change_password(request):
    if request.is_ajax():
        pass


#*******************************************************************************
# DASHBOARD
#*******************************************************************************    

@login_required
def dashboard(request,  usertype = None):

    data_dict = {}

    template = 'crm/dashboard.html'
    data_dict["css_files"] = []

    data_dict["js_files"] = [
                                "vendor/sparkline/index.js",
                                "vendor/flot/jquery.flot.min.js",
                                "vendor/flot/jquery.flot.resize.min.js",
                                "vendor/flot/jquery.flot.spline.js",
                            ]


    return render(request, '', data_dict)