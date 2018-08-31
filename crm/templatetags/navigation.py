from django import template

# Django settings from settings.py
from django.conf import settings

# Import models
from crm.models import *

# Condition operators for models
from django.db.models import Q, When
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone, safestring

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
# Filter for returning location of menu/sidebar/navigation template
#

@register.filter
def menu_template(value):
    value = int(value)
    nav_template = settings.BASE_DIR+"/crm/templates/crm/"

    try:
        usertype = User_usertype.objects.get(user_id = value)
        usertype_id = usertype.usertype_id

        try:
            nav_tmp = Usertype.objects.get(pk = usertype_id)

            if nav_tmp.use_nav_from_template_folder:
                nav_template += nav_tmp.template_folder +"/"+ nav_tmp.menu_template_name
            else:
                nav_template += nav_tmp.menu_template_name

        except User_usertype.DoesNotExist:
            pass 
        except TypeError: 
            pass       

    except User_usertype.DoesNotExist:
        pass    
    except TypeError: 
        pass
    return nav_template   


#
# Tag for loading css files
#

@register.simple_tag
def load_css_files(scripts = list()):

    html = ''

    for script in scripts:
        html += '<link rel="stylesheet" href="'+settings.STATIC_URL+script+'"/>'
        
    return safestring.mark_safe(html)


#
# Tag for loading javascript files
#

@register.simple_tag
def load_javascript_files(scripts = list()):

    html = '<script src="'+settings.STATIC_URL+'vendor/pacejs/pace.min.js'+'"></script>'
    html += '<script src="'+settings.STATIC_URL+'vendor/jquery/dist/jquery.min.js'+'"></script>'
    html += '<script src="'+settings.STATIC_URL+'vendor/bootstrap/js/bootstrap.min.js'+'"></script>'
    html += '<script src="'+settings.STATIC_URL+'vendor/toastr/toastr.min.js'+'"></script>'

    for script in scripts:
        html += '<script src="'+settings.STATIC_URL+script+'"></script>'

    html += '<script src="'+settings.STATIC_URL+'scripts/luna.js'+'"></script>'
        
    return safestring.mark_safe(html)