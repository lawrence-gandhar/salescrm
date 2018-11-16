from django import template

# Django settings from settings.py
from django.conf import settings

# Import models
from crm.models import *

# Condition operators for models
from django.db.models import Q, When
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone, safestring

# Helper File Import
from crm.helpers import *

# use Library
register = template.Library()

#
# InArray Filter
#
@register.filter
def InArray(value, arr):
    if len(arr)>0:
        if value in arr:
            return True
    return False 

@register.filter
def leads_counter(id, arr):
    for item in arr[0]:
        if item["status_id"] in arr[1] and item["status_id"] == id:
            return "$"+str(item["total"])
    else:
        return "$0"