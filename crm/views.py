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
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

# Django settings from settings.py
from django.conf import settings	

# Condition operators for models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# Other imports
from django.shortcuts import render, redirect

#from .models import Usertype, User_usertype

# Helper File Import
from crm.helpers import *

# system imports
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

            request.session["user_id"] = user.id

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

    template = 'crm/'+current_user_url(request.session["user_id"])+'/dashboard.html'
    data_dict["css_files"] = []

    data_dict["js_files"] = [
                                "vendor/sparkline/index.js",
                                "vendor/flot/jquery.flot.min.js",
                                "vendor/flot/jquery.flot.resize.min.js",
                                "vendor/flot/jquery.flot.spline.js",
                            ]


    return render(request, template, data_dict)


#*******************************************************************************
# ADD LEAD STEP - 1
#*******************************************************************************    

@login_required
def add_lead(request, usertype = None):

    template = 'crm/'+current_user_url(request.session["user_id"])+'/add_lead.html'

    data_dict = {}
    data_dict["css_files"] = []

    data_dict["js_files"] = []

    data_dict["lead_type"] = lead_type()
    data_dict["lead_line_of_business"] = lead_line_of_business()
    data_dict["lead_payment_type"] = lead_payment_type()
    data_dict["lead_probability"] = lead_probability()
    data_dict["country_list"] = country_list()

    #
    # ON POST OPERATION
    #

    submit = request.POST.get("submit", False)

    if submit:

        try:
            lead = Leads_tbl(
                company_name = request.POST["company_name"],
                contact_title = request.POST["contact_title"],
                contact_firstname = request.POST["contact_firstname"],
                contact_lastname = request.POST["contact_lastname"],
                contact_details = request.POST["contact_details"],
                contact_designation = request.POST["contact_designation"],
                address = request.POST["contact_address"],
                country = request.POST["country"],
                phone = request.POST["contact_phone"],
                extension = request.POST["contact_extension"],
                fax = request.POST["contact_fax"],
                email = request.POST["contact_email"],
                website = request.POST["contact_website"],
                lead_type = Lead_type(id = int(request.POST["lead_type"])),
                line_of_business = Lead_line_of_business(id = int(request.POST["lead_line_of_business"])),
                payment_type = Lead_payment_type(id = int(request.POST["payment_type"])),
                probability = Lead_probability(id = int(request.POST["probability"])),
                fte = request.POST["fte"],
                annual = request.POST["annual"],
            )

            lead.save()

            add_lead_logs(lead.id, request.session["user_id"], 'Lead Added')

            messages.error(request, 'Data Saved')
            return redirect("/"+current_user_url(request.session["user_id"]) + '/leads/add/2/'+str(lead.id))

        except:
            messages.error(request, 'Error Occurred!')
            return redirect("/"+current_user_url(request.session["user_id"]) + '/leads/add/')

    return render(request, template, data_dict)


#*******************************************************************************
# ADD LEAD STEP - 2
#*******************************************************************************    

@login_required
def add_lead_step_2(request, usertype = None, slug = None, step = 1,  id = None):

    #
    #   Check Slug - If slug is `add` and step = 1 then open disabled step 1 page
    #   if slug is `add` and step = 2 then disable page 1 and perform check
    #       if step 2 form is already filled then disable the template
    #       else enable the form for filling
    #

    #
    # common data
    #

    template = 'crm/'+current_user_url(request.session["user_id"])+'/edit_lead_step2.html'

    data_dict = {}
    data_dict["css_files"] = []

    data_dict["js_files"] = []

    data_dict["error"] = ""
    data_dict["error_2"] = ""

    #
    # ON GET OPERATION - Check lead Id exists or not across add and edit opeartions of form 1 and 2
    #

    try:
        lead = Leads_tbl.objects.get(pk = id)
    except Leads_tbl.DoesNotExist:
        data_dict["error"] = "Invalid Lead ID. Operation Denied!"
        return render(request, template, data_dict)    
 
    #
    # If lead exists fill form 1 details 
    #

    data_dict["company_name"] = lead.company_name
    data_dict["contact_title"] = lead.contact_title
    data_dict["contact_firstname"] = lead.contact_firstname
    data_dict["contact_lastname"] = lead.contact_lastname
    data_dict["contact_details"] = lead.contact_details
    data_dict["contact_designation"] = lead.contact_designation
    data_dict["address"] = lead.address
    data_dict["country_list"] = country_list([lead.country])
    data_dict["phone"] = lead.phone
    data_dict["extension"] = lead.extension
    data_dict["fax"] = lead.fax
    data_dict["email"] = lead.email
    data_dict["website"] = lead.website
    data_dict["fte"] = lead.fte
    data_dict["annual"] = lead.annual

    data_dict["lead_type"] = lead_type(lead.lead_type_id)
    data_dict["lead_line_of_business"] = lead_line_of_business(lead.line_of_business_id)
    data_dict["lead_payment_type"] = lead_payment_type(lead.payment_type_id)
    data_dict["lead_probability"] = lead_probability(lead.probability_id)

    #
    #   Form 2 fields will be always empty by default
    #

    data_dict["inbound_per_month"] = ""
    data_dict["outbound_per_month"] = ""
    data_dict["inbound_mins_per_call"] = ""
    data_dict["outbound_mins_per_call"] = ""
    data_dict["anticipated_date"] = ""
    data_dict["call_contact"] = "None"
    data_dict["product_service_description"] = ""
    data_dict["area_of_operation"] = country_list()
    data_dict["centers_interested"] = country_list()
    data_dict["work_hours"] = ""
    data_dict["pricing"] = ""
    data_dict["comments"] = ""

    if step == '1':
        data_dict["step_1"] = True
    else:
        data_dict["step_1"] = False

    #
    #   Check form 2 is already filled or not
    #
    try:
        lead_quest_present = Lead_questionnaire_model.objects.get(lead_id = id)
                
        if slug == "add":        
            data_dict["done"] = True    
        elif slug == "edit":
            data_dict["done"] = False
        else:
            return HttpResponse(status = 404)

        data_dict["lead_program_requirement"] = lead_program_requirement(lead_quest_present.qpr.split(','), 'qpr[]')
        data_dict["lead_call_purpose"] = lead_call_purpose(lead_quest_present.lcp.split(','), 'lcp[]')
        data_dict["lead_pricing_model"] = lead_pricing_model(lead_quest_present.lpm.split(','), 'lpm[]')

        data_dict["inbound_per_month"] = lead_quest_present.inbound_per_month
        data_dict["outbound_per_month"] = lead_quest_present.outbound_per_month
        data_dict["inbound_mins_per_call"] = lead_quest_present.inbound_mins_per_call
        data_dict["outbound_mins_per_call"] = lead_quest_present.outbound_mins_per_call
        data_dict["anticipated_date"] = lead_quest_present.anticipated_date
        data_dict["call_contact"] = lead_quest_present.call_contact
        data_dict["product_service_description"] = lead_quest_present.product_service_description
        data_dict["area_of_operation"] = country_list(lead_quest_present.area_of_operation.split(','))
        data_dict["centers_interested"] = country_list(lead_quest_present.centers_interested.split(','))
        data_dict["work_hours"] = lead_quest_present.work_hours
        data_dict["pricing"] = lead_quest_present.pricing
        data_dict["comments"] = lead_quest_present.comments

    except Lead_questionnaire_model.DoesNotExist:
        data_dict["done"] = False    
        data_dict["lead_program_requirement"] = lead_program_requirement([0], 'qpr[]')
        data_dict["lead_call_purpose"] = lead_call_purpose([0], 'lcp[]')
        data_dict["lead_pricing_model"] = lead_pricing_model([0], 'lpm[]')

    #
    # ON POST OPERATION
    #

    submit = request.POST.get("submit", False)

    if submit:

        if step == '1':

            try:
                lead_present = Leads_tbl.objects.get(pk = int(id))
                found_lead = True
            except Lead_questionnaire_model.DoesNotExist:
                found_lead = False

            lead_present.lead_type_id = request.POST["lead_type"]
            lead_present.company_name = request.POST["company_name"]
            lead_present.contact_title = request.POST["contact_title"]
            lead_present.contact_firstname = request.POST["contact_firstname"]
            lead_present.contact_lastname = request.POST["contact_lastname"]
            lead_present.contact_designation = request.POST["contact_designation"]
            lead_present.contact_details = request.POST["contact_details"]
            lead_present.address = request.POST["address"]
            lead_present.country = request.POST["country"]
            lead_present.phone = request.POST["phone"]
            lead_present.email = request.POST["email"]
            lead_present.extension = request.POST["extension"]
            lead_present.website = request.POST["website"]
            lead_present.fax = request.POST["fax"]
            lead_present.fte = request.POST["fte"]
            lead_present.annual = request.POST["annual"]
            lead_present.line_of_business_id = request.POST["lead_line_of_business"]
            lead_present.payment_type_id = request.POST["payment_type"]
            lead_present.probability_id = request.POST["probability"]

            try:
                lead_present.save()
                add_lead_logs(id, 'Lead Modified')
                messages.error(request, 'Data Saved')
                return redirect("/"+current_user_url(request.session["user_id"]) + '/leads/'+slug+'/'+step+'/' + str(id) +'/')
            except:
                data_dict["error_2"] = "Error Occurred. Saving Failed. Try Again!"   


        if step == '2':

            try:
                lead_present = Lead_questionnaire_model.objects.get(lead_id = int(id))
                found_lead = True
            except Lead_questionnaire_model.DoesNotExist:
                found_lead = False

            if found_lead:
                lead_present.qpr = ','.join(request.POST.getlist("qpr[]"))
                lead_present.lcp = ','.join(request.POST.getlist("lcp[]"))
                lead_present.lpm = ','.join(request.POST.getlist("lpm[]"))
                lead_present.inbound_per_month = int(request.POST["inbound_per_month"])
                lead_present.outbound_per_month = int(request.POST["inbound_per_month"])
                lead_present.inbound_mins_per_call = int(request.POST["inbound_mins_per_call"])
                lead_present.outbound_mins_per_call = int(request.POST["outbound_mins_per_call"])
                lead_present.call_contact = request.POST["call_contact"]
                lead_present.anticipated_date = request.POST["anticipated_date"]
                lead_present.product_service_description = request.POST["product_service_description"]
                lead_present.area_of_operation = ','.join(request.POST.getlist("area_of_operation"))
                lead_present.work_hours = request.POST["work_hours"]
                lead_present.centers_interested = ','.join(request.POST.getlist("centers_interested"))
                lead_present.pricing = float(request.POST["pricing"])
                lead_present.comments = request.POST["comments"]

                try:
                    lead_present.save()
                    add_lead_logs(id, request.session["user_id"], 'Lead Questionnaire Modified')
                    messages.error(request, 'Data Saved')
                    return redirect("/"+current_user_url(request.session["user_id"]) + '/leads/'+slug+'/'+step+'/' + str(id) +'/')
                except:
                    data_dict["error_2"] = "Error Occurred. Saving Failed. Try Again!"   

            else:
                lead_quest = Lead_questionnaire_model(
                    lead_id = int(id),
                    qpr = ','.join(request.POST.getlist("qpr[]")),
                    lcp = ','.join(request.POST.getlist("lcp[]")),
                    lpm = ','.join(request.POST.getlist("lpm[]")),
                    inbound_per_month = int(request.POST["inbound_per_month"]),
                    outbound_per_month = int(request.POST["inbound_per_month"]),
                    inbound_mins_per_call = int(request.POST["inbound_mins_per_call"]),
                    outbound_mins_per_call = int(request.POST["outbound_mins_per_call"]),
                    call_contact = request.POST["call_contact"],
                    anticipated_date = request.POST["anticipated_date"],
                    product_service_description = request.POST["product_service_description"],
                    area_of_operation = ','.join(request.POST.getlist("area_of_operation")),
                    work_hours = float(request.POST["work_hours"]),
                    centers_interested = ','.join(request.POST.getlist("centers_interested")),
                    pricing = float(request.POST["pricing"]),
                    comments = request.POST["comments"],
                )

                try: 
                    lead_quest.save()
                    add_lead_logs(id, request.session["user_id"], 'Lead Questionnaire Added')
                    messages.error(request, 'Data Saved')
                    return redirect("/"+current_user_url(request.session["user_id"]) + '/leads/'+slug+'/'+step+'/' + str(id) +'/')
                except:
                    data_dict["error_2"] = "Error Occurred. Saving Failed. Try Again!"

    return render(request, template, data_dict)


#*******************************************************************************
# MANAGE LEAD
#*******************************************************************************   
#   
@login_required
def manage_leads(request, usertype = None):
    template = 'crm/'+current_user_url(request.session["user_id"])+'/manage_leads.html'

    data_dict = {}
    data_dict["css_files"] = []

    data_dict["js_files"] = []

    data_dict["error"] = ""
    data_dict["country_json"] = country_json()

    leads = Leads_tbl.objects
    submit = request.POST.get('submit', False)

    if submit:
        leads = leads.filter(company_name__icontains=request.POST['company_name'])
    else:
        leads = leads.all()

    leads = leads.values('id', 'company_name', 'contact_title', 'contact_firstname', 'contact_lastname', 'address', 'country', 'contact_details', 'contact_designation', 'phone', 'fax', 'extension', 'phone', 'email', 'website', 'fte', 'annual','creation_date', 'last_updated', 'status__name', 'line_of_business__name', 'lead_type__name', 'payment_type__name', 'probability__name')
    
    paginator = Paginator(leads, 10) # Show 25 contacts per page

    page = request.GET.get('page')

    
    try:
        if page is None:
            page = 1
        leads = paginator.get_page(page)
        check = paginator.page(page)
    except InvalidPage:
        return render(request,'crm/error.html',{})
    except PageNotAnInteger:
            return render(request,'crm/error.html',{})
    except EmptyPage:
        return render(request,'crm/error.html',{}) 

    data_dict["leads"] = leads
    
    return render(request, template, data_dict)

#*******************************************************************************  
# FETCH LEAD QUESTIONNAIRE DETAILS
#*******************************************************************************  
#   
@login_required
def fetch_lead_details(request, usertype = None):
    if request.is_ajax():

        try:
            lead_queryset = Lead_questionnaire_model.objects.get(lead_id = int(request.POST["id"]))

            call_purpose = Lead_call_purpose.objects.filter(pk__in = lead_queryset.lcp.split(',')).values_list('name',flat=True)
            qpr_set = Lead_program_requirement.objects.filter(pk__in = lead_queryset.qpr.split(',')).values_list('name',flat=True)
            lpm_set = Lead_pricing_model.objects.filter(pk__in = lead_queryset.lpm.split(',')).values_list('name',flat=True)


            lead = {'id': lead_queryset.id, 
                    'qpr': ', '.join(qpr_set),
                    'lcp': ', '.join(call_purpose),
                    'lpm': ', '.join(lpm_set),
                    'inbound_per_month': lead_queryset.inbound_per_month,
                    'inbound_mins_per_call': lead_queryset.inbound_mins_per_call,
                    'outbound_per_month': lead_queryset.outbound_per_month,
                    'outbound_mins_per_call': lead_queryset.outbound_mins_per_call,
                    'call_contact': lead_queryset.call_contact,
                    'anticipated_date': lead_queryset.anticipated_date,
                    'product_service_description': lead_queryset.product_service_description,
                    'area_of_operation': lead_queryset.area_of_operation,
                    'work_hours': lead_queryset.work_hours,
                    'centers_interested': lead_queryset.centers_interested,
                    'pricing': lead_queryset.pricing,
                    'comments': lead_queryset.comments, 
                }

            return HttpResponse(json.dumps(lead))
        except Lead_questionnaire_model.DoesNotExist:
            return HttpResponse(0)

#
#   LEAD ASSIGNMENTS
#
@login_required
def lead_assignments(request, usertype = None):
    template = 'crm/'+current_user_url(request.session["user_id"])+'/projects.html'

    data_dict = {}
    data_dict["css_files"] = []

    data_dict["js_files"] = []

    leads = Leads_tbl.objects
    submit = request.POST.get('submit', False)

    if request.POST:
        leads = leads.filter(company_name__icontains=request.POST['company_name'])
    else:
        leads = leads.all()

    leads = leads.prefetch_related('assigned_to')
    
    #values('id', 'company_name', 'status__name', 'active', 'creation_date',)
    
    paginator = Paginator(leads, 25) # Show 25 contacts per page

    page = request.GET.get('page')

    try:
        if page is None:
            page = 1
        leads = paginator.get_page(page)
        check = paginator.page(page)
    except InvalidPage:
        return render(request,'crm/error.html',{})
    except PageNotAnInteger:
            return render(request,'crm/error.html',{})
    except EmptyPage:
        return render(request,'crm/error.html',{}) 

    data_dict["leads"] = leads

    return render(request, template, data_dict)


#
#   LEAD ASSIGNMENTS
#
@login_required
def lead_assignments_edit(request, usertype = None, id = None):
    template = 'crm/'+current_user_url(request.session["user_id"])+'/edit_assignments.html'

    data_dict = {}
    data_dict["css_files"] = []

    data_dict["js_files"] = []

    users_present = Leads_tbl.objects.get(pk = int(id))

    users_present_now = users_present.assigned_to.all().values_list('id', flat = True)

    users_present_list = users_present.assigned_to.all().values('id', 'first_name', 'last_name', 'email')

    data_dict["users_present_list"] = users_present_list

    try:
        user_type = Usertype.objects.get(name__iexact = 'Agent')

        agents = User_usertype.objects.filter(usertype_id = user_type.id).values_list('user_id', flat= True)
        
        users = User.objects.filter(id__in = agents).exclude(id__in = users_present_now).values('id', 'first_name', 'last_name', 'email')

        data_dict["users"] = users

    except Usertype.DoesNotExist:
        data_dict["users"] = {}


    if request.POST:

        user_list = request.POST.getlist('users_list[]')

        user = User.objects.filter(id__in = user_list)

        lead = Leads_tbl.objects.get(pk = int(id))
        lead.assigned_to.set(user)
        lead.save()

    return render(request, template, data_dict)


#
#   LEAD LOG, PROGRESS AND TIMELINE
#
@login_required
def timeline(request, usertype = None, id = None):
    template = 'crm/'+current_user_url(request.session["user_id"])+'/timeline.html'

    data_dict = {}
    data_dict["css_files"] = []

    data_dict["js_files"] = []

    lead_logs = Lead_logs.objects.filter(lead_id = id).values('lead_id', 'creation_date', 'notes', 'user__first_name', 'user__last_name').order_by('creation_date')

    data_dict['lead_id'] = id
    data_dict['lead_logs'] = lead_logs

    return render(request, template, data_dict)