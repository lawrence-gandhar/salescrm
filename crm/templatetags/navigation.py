from django import template

# Django settings from settings.py
from django.conf import settings

# Import models
from crm.models import *

# Condition operators for models
from django.db.models import Q, When
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone

# use Library
register = template.Library()


#
# Usertype Links
#
@register.filter
def link(value):
    try:
        url = Usertype.objects.get(pk = value)
        link = url.sub_link
    except ObjectDoesNotExist:
        link = ''

    return link            


#
# assessment links
#  
@register.filter   
def dynamic_links(value):
    return value.lower().replace(" ","-")

#
# Page title 
#   
@register.simple_tag 
def page_title():
    return settings.PAGE_TITLE

#
# Tag to return url prefix based on user type
#

@register.simple_tag
def current_user_link(value):
    value = int(value)
    link = ''

    try:
        url = Usertype.objects.get(pk = value)
        link = url.sub_link
    except:
        pass
    return link


#
# Filter for returning location of menu/sidebar/navigation template
#

@register.filter
def menu_template(value):
    value = int(value)
    nav_template = settings.BASE_DIR+"/app/templates/crm/"

    try:
        nav_tmp = Usertype.objects.get(pk = value)

        if nav_tmp.use_nav_from_template_folder:
            nav_template += nav_tmp.template_folder +"/"+ nav_tmp.menu_template_name
        else:
            nav_template += nav_tmp.menu_template_name   
    except:
        pass
    return nav_template    