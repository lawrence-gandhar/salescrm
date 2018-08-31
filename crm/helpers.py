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
#from .models import Assessment_Settings, AssessmentFormOptions, AssessmentFormQuestions, AssessmentFormSection

# system related imports
import sys, os, csv, json, datetime

#
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