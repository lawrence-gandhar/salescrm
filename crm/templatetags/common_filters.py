from django import template

# Django settings from settings.py
from django.conf import settings

# Import models
from crm.models import *
from django.contrib.auth.models import User

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

@register.filter
def contacts_meeting_at_hand(id, arr):
    for item in arr:
        if id == item.contact_id:
            return True
    else:
        return False

@register.simple_tag
def meeting_logs(id):
	html = list()

	meeting_logs = Meeting_logs.objects.filter(meeting_id = int(id)).values()
	print(meeting_logs)
	for item in meeting_logs:
		if item["log_type"] == "CANCELLED":
			cancelled_meetings = Cancelled_meetings.objects.filter(pk = int(item["record_id"])).select_related('user')
			
			print(cancelled_meetings)

			for i in cancelled_meetings:				
				html.append("<p>Meeting was <strong style='color:#FFFFFF'>"+ item["log_type"]+"</strong> ") 
				html.append("on <strong style='color:#FFFFFF'>" +item["created_on"].strftime('%b %d, %Y')+ "</strong> ")
				html.append("by <strong style='color:#FFFFFF'>" + i.user.first_name +" "+ i.user.last_name + "</strong> ")
				html.append("due to <strong style='color:#FFFFFF'>" + i.reason + "</strong></p>")
			

		if item["log_type"] == "POSTPONED":
			postponed_meetings = Postponed_meetings.objects.filter(pk = int(item["record_id"])).values()

			for i in postponed_meetings:
				html.append("<p>Meeting was <strong style='color:#FFFFFF'>"+ item["log_type"]+"</strong> ") 
				html.append("on <strong style='color:#FFFFFF'>" +item["created_on"].strftime('%b %d, %Y')+ "</strong> ")
				html.append("due to <strong style='color:#FFFFFF'>" + i["reason"] + "</strong></p>")

		if item["log_type"] == "ADJOURNED":
			adjourned_meetings = Adjourned_meetings.objects.filter(pk = int(item["record_id"])).values()

			for i in adjourned_meetings:
				html.append("<p>Meeting was <strong style='color:#FFFFFF'>"+ item["log_type"] +"</strong> due to <strong style='color:#FFFFFF'>" + i["reason"] + "</strong></p>")
				pass

		if item["log_type"] == "RESCHEDULED":
			rescheduled_meetings = Rescheduled_meetings.objects.filter(pk = int(item["record_id"])).values()

			for i in rescheduled_meetings:
				html.append("<p>Meeting was <strong style='color:#FFFFFF'>"+ item["log_type"] +"</strong></p>")
				pass


	return safestring.mark_safe(''.join(html))