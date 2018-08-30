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

#from .models import Usertype, Location, CustomUser, Department, Designation
#from .models import Assessment_Settings, AssessmentFormOptions, AssessmentFormQuestions, AssessmentFormSection

import sys, os, csv, json, datetime

#
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, 'crm/login.html', {})
