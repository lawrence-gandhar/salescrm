from django import template

# Django settings from settings.py
from django.conf import settings

# Import models
from crm.models import *

# use Library
register = template.Library()

#
# Tag for loading profile pics files
#

@register.simple_tag
def user_profile_pic(value):
    try:
        user = User.objects.get(pk = int(value))

        profile_pic = User_profile.objects.get(user = user.id)
        return settings.MEDIA_URL+str(profile_pic.photo)
        #return mark_safe('<img src="'+settings.MEDIA_URL+str(profile_pic.photo)+'" class="img-circle">')
    except:
        #return mark_safe('<img src="'+settings.MEDIA_URL+'download.jpg" class="img-circle">')
        return settings.MEDIA_URL+'download.jpg'