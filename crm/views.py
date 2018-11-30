# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# IntegrityError Exception for checking duplicate entry, 
# connection import to establish connection to database 
from django.db import IntegrityError, connection 

# Used for serializing object data to json string
from django.core.serializers.json import DjangoJSONEncoder 
from django.core.serializers import serialize

from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect, JsonResponse

# Paginator class import
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

# Django settings from settings.py
from django.conf import settings	

# Condition operators for models
from django.db.models import Q, Count, Sum, Prefetch
from django.core.exceptions import ObjectDoesNotExist

# Other imports
from django.shortcuts import render, redirect

#from .models import Usertype, User_usertype

# Helper File Import
from crm.helpers import *

# system imports
import sys, os, csv, json, datetime
from django.utils import timezone

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

                request.session["usertype_id"] = usertype.usertype_id

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
# DECORATOR FOR CHECKING URL AUTHENTICATION  
#******************************************************************************* 
#
def user_access_check(function=None):
    def check_me(*args, **kwargs):
        try:
            target_link = Usertype.objects.get(pk = int(args[0].session["usertype_id"]))
            url_link = target_link.sub_link

            if url_link != kwargs["usertype"]:
                logout(args[0])
                return HttpResponseRedirect('/')
        except:
            logout(args[0])
            return HttpResponseRedirect('/')
        return function(args[0], **kwargs)
    return check_me


#*******************************************************************************
# LOGOUT  
#*******************************************************************************   
#
@user_access_check
@login_required
def user_logout(request, usertype = None):
    logout(request)
    return HttpResponseRedirect('/')   


#*******************************************************************************
# PASSWORD CHANGE
#*******************************************************************************  
#   
@user_access_check
@login_required
def change_password(request):
    if request.is_ajax():
        pass


#*******************************************************************************
# DASHBOARD
#*******************************************************************************    
#

@user_access_check
@login_required
def dashboard(request,  usertype = None):

    data_dict = {}

    template = 'crm/'+current_user_url(request.session["user_id"])+'/dashboard.html'
    data_dict["css_files"] = []

    data_dict["js_files"] = [
                                "vendor/d3/d3.min.js",
                                "vendor/topojson/topojson.min.js",
                                "vendor/datamaps/datamaps.world.min.js",
                                "vendor/chart.js/dist/Chart.min.js",
                            ]

    #
    #   Check System Settings
    #
    data_dict["show_counters"] = True
    data_dict["show_bar_graphs"] = True
    data_dict["show_line_charts"] = True
    data_dict["show_geo_graph"] = True
    data_dict["show_geo_list"] = True
    data_dict["show_geo_list_filters"] = True
    data_dict["show_custom_counters"] = False

    try:
        dashboard_settings = Dashboard_Settings.objects.get(user_id = int(request.session["user_id"]))
        data_dict["show_counters"] = dashboard_settings.counters
        data_dict["show_bar_graphs"] = dashboard_settings.bar_graphs
        data_dict["show_line_charts"] = dashboard_settings.line_charts
        data_dict["show_geo_graph"] = dashboard_settings.geo_graph
        data_dict["show_geo_list"] = dashboard_settings.geo_list
        data_dict["show_geo_list_filters"] = dashboard_settings.geo_list_filters
    except:
        pass

    
    data_dict["lead_status"] = {"Others":0}
    data_dict["lead_active"] = {"Active":0, "Inactive":0}

    if data_dict["show_counters"] :
        counters = Counters_Settings.objects.filter(user_id =  int(request.session["user_id"]))

        if counters.count() > 0:
            data_dict["show_custom_counters"] = True
            data_dict["lead_status"] = {}
            for counter in counters:

                leads = Leads_tbl.objects.filter(status_id = int(counter.lead_status_id)).values('status_id')
                if counter.filters:
                    leads = leads.filter(active = 1)
                leads = leads.annotate(total = Count('status_id')).order_by()
                
                try:
                    status = Lead_status.objects.get(pk = int(counter.lead_status_id)) 
                    data_dict["lead_status"][status.name] = 0  

                    for lead in leads:
                        if lead["total"]:
                            data_dict["lead_status"][status.name] = lead["total"]
                except:
                    pass
        else:
            leads = Leads_tbl.objects.all()
            for lead in leads:

                if lead.status.name in data_dict["lead_status"].keys():
                    if lead.status.name in ["New", "Closed", "Reject"]:
                        data_dict["lead_status"][lead.status.name] += 1 
                else:
                    if lead.status.name in ["New", "Closed", "Reject"]:
                        data_dict["lead_status"][lead.status.name] = 1
                    else:
                        data_dict["lead_status"]["Others"] += 1
                
                if lead.active == 1:
                    data_dict["lead_active"]["Active"] += 1
                else:
                    data_dict["lead_active"]["Inactive"] += 1

    

    leads_for_countries = Leads_tbl.objects.all()
    
    with open(settings.BASE_DIR+'/crm/static/scripts/country_codes_2.json') as json_file:  
        country_codes = json.load(json_file)

    
    leads_generated_from_countries = {}
    leads_centers_interested = {}
    leads_area_of_operation = {}

    for lead in leads_for_countries:

        try:
            lead_questionnaire_model = Lead_questionnaire_model.objects.get(lead_id = lead.id)
            centers = lead_questionnaire_model.centers_interested.split(",")
            area_of_operation = lead_questionnaire_model.area_of_operation.split(",")

            for i in centers:
                if country_codes[i]["alpha-3"] in leads_centers_interested:
                    leads_centers_interested[country_codes[i]["alpha-3"]]["counter"] += 1
                else:
                    leads_centers_interested[country_codes[i]["alpha-3"]] = {"counter":1, 
                                                "name":country_codes[i]["name"], 
                                                "centered":country_codes[i]["alpha-3"],
                                                "fillKey":"active",}

            for i in area_of_operation:
                if country_codes[i]["alpha-3"] in leads_area_of_operation:
                    leads_area_of_operation[country_codes[i]["alpha-3"]]["counter"] += 1
                else:
                    leads_area_of_operation[country_codes[i]["alpha-3"]] = {"counter":1, 
                                                "name":country_codes[i]["name"], 
                                                "centered":country_codes[i]["alpha-3"],
                                                "fillKey":"active",}
        except:
            pass



        if country_codes[lead.country]["alpha-3"] in leads_generated_from_countries:
            leads_generated_from_countries[country_codes[lead.country]["alpha-3"]]["counter"] += 1
        else:
            leads_generated_from_countries[country_codes[lead.country]["alpha-3"]] = {"counter":1, 
                                        "name":country_codes[lead.country]["name"], 
                                        "centered":country_codes[lead.country]["alpha-3"],
                                        "fillKey":"active",}                                



    data_dict["leads_generated_from_countries"] = leads_generated_from_countries
    data_dict["leads_centers_interested"] = leads_centers_interested
    data_dict["leads_area_of_operation"] = leads_area_of_operation

    return render(request, template, data_dict)


#*******************************************************************************
# ADD LEAD STEP - 1
#*******************************************************************************    
#   
@user_access_check
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
#   
@user_access_check
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
                add_lead_logs(id, request.session["user_id"], 'Lead Modified')
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
@user_access_check   
@login_required
def manage_leads(request, usertype = None):
    template = 'crm/'+current_user_url(request.session["user_id"])+'/manage_leads.html'

    data_dict = {}
    data_dict["css_files"] = []

    data_dict["js_files"] = []

    data_dict["error"] = ""
    data_dict["country_json"] = country_json()
    data_dict["back_link"] = 'crm/'+current_user_url(request.session["user_id"])+'/leads/manage/'

    leads = Leads_tbl.objects
    submit = request.POST.get('submit', False)

    if submit:
        leads = leads.filter(company_name__icontains=request.POST['company_name'])

        if request.session["usertype_id"] == 2:
            leads = leads.filter(assigned_to = request.session["user_id"])
        else:
            leads = leads.all()
    else:
        if request.session["usertype_id"] == 2:
            leads = leads.filter(assigned_to = request.session["user_id"])
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
        return render(request,'crm/error.html',data_dict)
    except PageNotAnInteger:
            return render(request,'crm/error.html',data_dict)
    except EmptyPage:
        return render(request,'crm/error.html',data_dict) 

    data_dict["leads"] = leads
    
    return render(request, template, data_dict)

#*******************************************************************************  
# FETCH LEAD QUESTIONNAIRE DETAILS
#*******************************************************************************  
#   
@user_access_check  
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

#*******************************************************************************  
#   LEAD ASSIGNMENTS
#*******************************************************************************  
#   
@user_access_check
@login_required
def lead_assignments(request, usertype = None):
    template = 'crm/'+current_user_url(request.session["user_id"])+'/projects.html'

    data_dict = {}
    data_dict["css_files"] = []

    data_dict["js_files"] = []

    data_dict["lead_status"] = lead_status()

    leads = Leads_tbl.objects

    if request.POST:
        company_name = request.POST.get('company_name', False)
        lead_status_id = request.POST.get('lead_status', '0')
        
        if company_name:
            leads = leads.filter(company_name__icontains = company_name)

        if lead_status_id != '0':
            leads = leads.filter(status_id = int(lead_status_id))

        if request.POST["active_inactive"] !="2": 
            active_inactive = request.POST.get('active_inactive', True)  

            leads = leads.filter(active = active_inactive)

    else:
        leads = leads.all()

    leads = leads.prefetch_related('assigned_to')
    
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


#*******************************************************************************  
#   LEAD ASSIGNMENTS EDIT
#*******************************************************************************  
#   
@user_access_check
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

        removed_users = list(set(users_present_now) - (set(list(map(lambda x: int(x), user_list)))))
        

        lead.assigned_to.set(user)
        lead.save()

        log = ['Lead Assignment Performed']
        
        log.append('<br/>')
        for u in user:
            log.append('<br/><small style="font-size:80%;color:#f5a212">Added : '+u.first_name +" "+ u.last_name+'</small>')

        if len(user) == 0:
            log.append('<br/><small style="font-size:80%;color:#f5a212">Agents unassigned or a blank submission done</small>')

        if len(removed_users) > 0:
            for i in removed_users:
                rem = User.objects.get(pk = int(i))
                log.append('<br/><small style="font-size:80%;color:#f5a212">Removed : '+rem.first_name +" "+ rem.last_name+'</small>')

        log.append('<br/>')

        add_lead_logs(id, request.session["user_id"], ''.join(log))

        return redirect("/"+current_user_url(request.session["user_id"]) + '/leads/edit-assignment/' + str(id) +'/', True)

    return render(request, template, data_dict)


#*******************************************************************************  
#   LEAD LOG, PROGRESS AND TIMELINE
#*******************************************************************************  
#   
@user_access_check
@login_required
def timeline(request, usertype = None, id = None):
    template = 'crm/'+current_user_url(request.session["user_id"])+'/timeline.html'

    data_dict = {}
    data_dict["css_files"] = []

    data_dict["js_files"] = []

    lead_logs = Lead_logs.objects.filter(lead_id = id).values('lead_id', 'creation_date', 'notes', 'user__first_name', 'user__last_name').order_by('-creation_date')

    data_dict['lead_id'] = id
    data_dict['lead_logs'] = lead_logs

    return render(request, template, data_dict)

#*******************************************************************************  
#   LEAD MULTIPLE/SINGLE STATUS SET
#*******************************************************************************  
#   
@user_access_check
@login_required
def lead_multiple_status_set(request, usertype = None):
    if request.is_ajax():

        ids = request.POST.getlist('case')

        for id in ids:
            try:
                lead = Leads_tbl.objects.get(pk = int(id))
                lead.status_id = int(request.POST["lead_status"])
                lead.save()

                log = ['Lead Status Modified']
                log.append('<br/><small style="font-size:80%;color:#f5a212">Status Set : '+lead.status.name+'</small>')
                add_lead_logs(id, request.session["user_id"], ''.join(log))
            except:
                return HttpResponse(0)
        return HttpResponse(1)
    return HttpResponse(0)

#*******************************************************************************  
#   LEAD MULTIPLE ACTIVE IN-ACTIVE SET
#*******************************************************************************  
#   
@user_access_check
@login_required
def lead_multiple_active_set(request, usertype = None):
    if request.is_ajax():

        ids = request.POST.getlist('case')
    
        for id in ids:
            try:
                lead = Leads_tbl.objects.get(pk = int(id))
                lead.active = int(request.POST["lead_active"])
                lead.save()

                log = ['Lead Active/In-Active Modified']
                if int(request.POST["lead_active"]) == 1: 
                    log.append('<br/><small style="font-size:80%;color:#f5a212">Lead Set to ACTIVE</small>')
                else:
                    log.append('<br/><small style="font-size:80%;color:#f5a212">Lead Set to IN-ACTIVE</small>')
                add_lead_logs(id, request.session["user_id"], ''.join(log))
            except:
                return HttpResponse(0)
        return HttpResponse(1)
    return HttpResponse(0)

#*******************************************************************************  
#   LEAD MESSAGES
#*******************************************************************************  
#   
@user_access_check
@login_required
def lead_messages(request, usertype = None, id = None):
    template = 'crm/'+current_user_url(request.session["user_id"])+'/messages.html'

    data_dict = {}
    data_dict["css_files"] = ["vendor/summernote/dist/summernote.css"]

    data_dict["js_files"] = ['vendor/summernote/dist/summernote.min.js']

    lead_messages = Lead_message.objects.filter(lead_id = id).values('lead_id', 'creation_date', 'message', 'user__first_name', 'user__last_name').order_by('-creation_date')

    data_dict['lead_id'] = id
    data_dict['lead_messages'] = lead_messages

    return render(request, template, data_dict)        

#*******************************************************************************  
#   LEAD MESSAGE ADD
#*******************************************************************************  
#   
@user_access_check    
@login_required
def lead_message_add(request, usertype = None):
    if request.is_ajax():
        if request.POST["message"].strip() !="":
            try:
                lead = Leads_tbl.objects.get(pk = int(request.POST["lead_id"]))
                
                lead_message = Lead_message(
                    lead_id = lead.id,
                    message = request.POST["message"],
                    user_id = request.session["user_id"]
                )
                lead_message.save()

                users = lead.assigned_to.all().values_list('id', flat = True)
                
                for user in users:
                    if int(user) != int(request.session["user_id"]):
                        lead_messsage_log = Lead_message_log(
                            message_id = lead_message.id,
                            user_id = int(user)
                        )

                        lead_messsage_log.save()

                log = ['Lead Message Added']
                log.append('<br/><small style="font-size:80%;color:#f5a212">'+request.POST["message"]+'</small>')
                add_lead_logs(id, request.session["user_id"], ''.join(log))    
            except:
                return HttpResponse(0)
            return HttpResponse(1)
        return HttpResponse(0)
    return HttpResponse(0)

#*******************************************************************************  
#   DOCUMENTATION
#*******************************************************************************  
# 
@user_access_check
@login_required
def lead_stats(request, usertype = None):
    template = 'crm/leads_stats.html'

    data_dict = {}
    data_dict["css_files"] = []
    data_dict["js_files"] = ['vendor/select2/dist/js/select2.js']

    lead_status = request.POST.getlist("lead_status")
    lead_status_order = Lead_status.objects.filter(active = True)

    lead_status_list = Lead_status.objects.filter(active = True)

    if len(lead_status) > 0:
        lead_status_order = lead_status_order.filter(id__in = lead_status)
        leads = Leads_tbl.objects.filter(status__in = lead_status, active = 1).values()
        counters = Leads_tbl.objects.filter(status__in = lead_status, active = 1).values('status_id').annotate(counters = Count('status_id'),  total = Sum('annual')).order_by()

    else:
        leads = Leads_tbl.objects.filter(active = 1).values()
        counters = Leads_tbl.objects.filter(active = 1).values('status_id').annotate(counters = Count('status_id'),  total = Sum('annual')).order_by()

    data_dict["status_array"] = []
    for item in lead_status_list:
        data_dict["status_array"].append(item.id)
    
    
    data_dict["lead_status_order"] = lead_status_order
    data_dict["lead_status_list"] = lead_status_list
    data_dict["leads"] = leads
    data_dict["status_array"] = (counters, data_dict["status_array"])

    return render(request, template, data_dict) 


#*******************************************************************************  
#   DOCUMENTATION
#*******************************************************************************  
#   
@user_access_check     
@login_required
def documentation(request, usertype = None):
    template = 'crm/'+current_user_url(request.session["user_id"])+'/support.html'

    data_dict = {}
    data_dict["css_files"] = []

    data_dict["js_files"] = []

    return render(request, template, data_dict)        

#*******************************************************************************
#   SYSTEM SETTINGS
#*******************************************************************************
#
@user_access_check     
@login_required
def system_settings(request, usertype = None):
    template = 'crm/system_settings.html'

    data_dict = {}
    data_dict["css_files"] = []

    data_dict["js_files"] = []

    #*******************************************
    #   Dashboard Settings
    #*******************************************
    try:
        dashboard_settings_data = Dashboard_Settings.objects.get(user_id = int(request.session["user_id"]))

        data_dict["counters"] = dashboard_settings_data.counters
        data_dict["line_charts"] = dashboard_settings_data.line_charts
        data_dict["bar_graphs"] = dashboard_settings_data.bar_graphs
        data_dict["geo_graph"] = dashboard_settings_data.geo_graph
        data_dict["geo_list"] = dashboard_settings_data.geo_list
        data_dict["geo_list_filters"] = dashboard_settings_data.geo_list_filters
        
    except:
        data_dict["counters"] = False
        data_dict["line_charts"] = False
        data_dict["bar_graphs"] = False
        data_dict["geo_graph"] = False
        data_dict["geo_list"] = False
        data_dict["geo_list_filters"] = False

    #*******************************************
    #   Counter Settings
    #*******************************************
    counters_settings_data = Counters_Settings.objects.filter(user_id = int(request.session["user_id"])).values()

    data_dict["counters_settings_data"] = dict({"counters_customization":False})
    lead_status = {}
    for item in counters_settings_data:
        data_dict["counters_settings_data"]["counters_customization"] = item["counters_customization"]
        lead_status[item["lead_status_id"]] = item["filters"]
        
    data_dict["counters_settings_data"]["lead_status"] = lead_status

    #*******************************************
    #   Lead Status List
    #*******************************************
    data_dict["lead_status_list"] = Lead_status.objects.filter(active = 1).values('id','name')    
    
    return render(request, template, data_dict)    


#*******************************************************************************
#   DASHBOARD SETTINGS
#*******************************************************************************
#
@user_access_check     
@login_required
def dashboard_settings(request, usertype = None):
 
    if request.is_ajax():

        counters = request.POST.get("counters", False)
        line_charts = request.POST.get("line_charts", False)
        bar_graphs = request.POST.get("bar_graphs", False)
        geo_graph = request.POST.get("geo_graph", False)
        geo_list = request.POST.get("geo_list", False)
        geo_list_filters = request.POST.get("geo_list_filters", False)

        try:
            dashboard_settings = Dashboard_Settings.objects.get(user_id = int(request.session["user_id"]))

            dashboard_settings.user_id = int(request.session["user_id"])
            dashboard_settings.counters = counters
            dashboard_settings.line_charts = line_charts
            dashboard_settings.bar_graphs = bar_graphs
            dashboard_settings.geo_graph = geo_graph
            dashboard_settings.geo_list = geo_list
            dashboard_settings.geo_list_filters = geo_list_filters
        except:
            dashboard_settings = Dashboard_Settings(
                user_id = int(request.session["user_id"]),
                counters = counters,
                line_charts = line_charts,
                bar_graphs = bar_graphs,
                geo_graph = geo_graph,
                geo_list = geo_list,
                geo_list_filters = geo_list_filters,
            )
        dashboard_settings.save()
        return HttpResponse(1)   
    return HttpResponse(0)   

#*******************************************************************************
# COUNTER CUSTOMIZATION
#*******************************************************************************
#
@user_access_check     
@login_required
def counters_customization(request, usertype = None):
    if request.is_ajax():

        Counters_Settings.objects.filter(user_id = int(request.session["user_id"])).delete()

        customize_counters = request.POST.get('customize_counters', False)
        lead_status = request.POST.getlist('lead_status[]')
        filters = request.POST.getlist('lead_status_active[]') 

        if customize_counters:
            main_tup = [] 
            for id in lead_status:
                if id in filters:
                    main_tup.append((id,1))
                else:
                    main_tup.append((id,0))

            for i,j in main_tup:
                counters = Counters_Settings( 
                    user_id = int(request.session["user_id"]),
                    counters_customization = int(customize_counters),
                    lead_status_id = int(i),
                    filters = int(j)
                )
                counters.save()    
        return HttpResponse(1)
    return HttpResponse(0)

#*******************************************************************************
# CONTACTS
#*******************************************************************************
#
@user_access_check     
@login_required
def contacts(request, usertype = None, view_type = None):

    data_dict = {}
    data_dict["css_files"] = []
    data_dict["view_type"] = view_type
    data_dict["back_link"] = "/"+ current_user_url(request.session["user_id"]) + "/contacts/"+view_type+"/"

    print(data_dict["back_link"])

    data_dict["js_files"] = ["vendor/bootstrap3-typeahead/bootstrap3-typeahead.min.js"]

    data_dict["contacts"] = Contacts.objects.all().order_by('id')

    if view_type == 'list':
        template = 'crm/contacts_list.html'
        paginator = Paginator(data_dict["contacts"], 10) # Show 10 contacts per page
    if view_type == 'grid':
        template = 'crm/contacts.html'
        paginator = Paginator(data_dict["contacts"], 15) # Show 15 contacts per page

    startdate = timezone.now()
    enddate = startdate + datetime.timedelta(days=7)
    data_dict["contacts_meeting"] = Contacts_meeting.objects.filter(meeting_schedule__range=[startdate, enddate])
    
    data_dict["company_names"] = list()
    for item in data_dict["contacts"]:
        data_dict["company_names"].append(item.company_name.lower())

    if request.POST:
        contacts = Contacts(
            company_name = request.POST["company_name"],
            contact_title = request.POST["contact_title"],
            contact_person = request.POST["contact_person"],
            job_title = request.POST["job_title"],
            address = request.POST["address"],
            contact_phone = request.POST["contact_phone"],
            contact_email = request.POST["contact_email"],
            contact_website = request.POST["contact_website"],
            comment = request.POST["comment"],
        )
        
        contacts.save()
        return redirect("/"+ current_user_url(request.session["user_id"]) + "/contacts/"+view_type+"/")

    # pagination 
    #

    page = request.GET.get('page')

    try:
        if page is None:
            page = 1
        data_dict["contacts"] = paginator.get_page(page)
        check = paginator.page(page)
    except InvalidPage:
        return render(request,'crm/error.html',data_dict)
    except PageNotAnInteger:
            return render(request,'crm/error.html',data_dict)
    except EmptyPage:
        return render(request,'crm/error.html', data_dict) 

    return render(request, template, data_dict)  


#*******************************************************************************
# CONTACTS EDIT
#*******************************************************************************
#
@user_access_check     
@login_required
def contacts_save_data(request, usertype = None):
    if request.is_ajax():

        company_name = request.POST.get('company_name','')
        contact_title = request.POST.get('contact_title','')
        contact_person = request.POST.get('contact_person','')
        job_title = request.POST.get('job_title','')
        address = request.POST.get('address','')
        contact_phone = request.POST.get('contact_phone','')
        contact_email = request.POST.get('contact_email','')
        contact_website = request.POST.get('contact_website','')
        comment = request.POST.get('comment','')

        try:
            contacts = Contacts.objects.get(pk = int(request.POST["id"]))
            contacts.company_name = company_name
            contacts.contact_title = contact_title
            contacts.contact_person = contact_person
            contacts.job_title = job_title
            contacts.address = address
            contacts.contact_phone = contact_phone
            contacts.contact_email = contact_email
            contacts.contact_website = contact_website
            contacts.comment = comment
            contacts.save()

            return HttpResponse(1) 
        except:
            return HttpResponse(0)     
    return HttpResponse(0)


#*******************************************************************************
# CONTACTS GET DATA
#*******************************************************************************
#
@user_access_check     
@login_required
def contacts_get_data(request, usertype = None):
    if request.is_ajax():

        try:
            contacts = Contacts.objects.get(pk = int(request.POST["id"]))
            
            data = dict({
                    "company_name":contacts.company_name, 
                    "contact_title" : contacts.contact_title, 
                    "contact_person" : contacts.contact_person,
                    "job_title" : contacts.job_title,
                    "address" : contacts.address, 
                    "contact_phone" : contacts.contact_phone, 
                    "contact_email" : contacts.contact_email,
                    "contact_website" : contacts.contact_website,
                    "comment" : contacts.comment, 
                })
            return HttpResponse(json.dumps(data))
        except:
            return HttpResponse(0)
    return HttpResponse(0)



#*******************************************************************************
# MEETING SCHEDULE
#*******************************************************************************
#
@user_access_check     
@login_required
def meetings_scheduled(request, usertype = None, contact_id = None):

    template = 'crm/meetings_schedule.html'
    error_template = 'crm/error.html'
    
    data_dict = {}
    data_dict["css_files"] = []

    data_dict["js_files"] = ['vendor/select2/dist/js/select2.js']

    data_dict["back_link"] = '/'+current_user_url(request.session["user_id"]) + '/contacts/list/'
    data_dict["company_name"] = ''
    data_dict["contact_id"] = contact_id

    #
    #   GET USER LIST WITH PICTURES
    #
    data_dict["user_lists"] = User.objects.filter(is_active = True, is_superuser = False).values('id', 'username', 'first_name', 'last_name')
    data_dict["meeting_schedules"] = None

    contact = None
    if contact_id is not None:
       
        try:
            contact = Contacts.objects.get(pk = int(contact_id))
        except:
            template =  error_template

        if contact is not None:
            data_dict["company_name"] = contact.company_name

            #
            #
            contacts_meeting = Contacts_meeting.objects.filter(contact = contact.id).select_related('scheduled_by').order_by('-meeting_schedule')

            data_dict["meetings"] = {}
            meetings_list = list()
            i = 0
            for meeting in contacts_meeting:

                meetings_list.append({
                    'meeting_id' : meeting.id,
                    'contact_id' : meeting.contact_id,
                    'scheduled_by_id' : meeting.scheduled_by_id,
                    'scheduled_by' : meeting.scheduled_by.first_name +" "+ meeting.scheduled_by.last_name,
                    'meeting_schedule' : meeting.meeting_schedule,
                    'agenda' : meeting.agenda,
                    'meeting_created_on' : meeting.created_on,
                    'meeting_attendees' : list()
                })                  

                attendees = Meeting_attendees.objects.filter(meeting = meeting.id).select_related('user')

                attend = list()
                for members in attendees:
                    attend.append({
                        'id' : members.user.id,
                        'name' : members.user.first_name +" "+members.user.last_name
                    })
                meetings_list[i]['meeting_attendees'] = attend
                
                pass

                i += 1 
            data_dict["meetings"] = meetings_list
    #
    #   MEETING SCHEDULE ADD
    #
    if request.POST:

        meetings_sch = Contacts_meeting(
            agenda = request.POST["agenda"],
            contact_id = int(request.POST["id"]),
            scheduled_by_id = int(request.session["user_id"]),
            meeting_schedule = request.POST["meeting_date"] +" "+request.POST["meeting_time"]+":00"
        )

        meetings_sch.save()

        attendees = request.POST.getlist('attendees') 

        if len(attendees) > 0:
            for user in attendees:
                meeting_attendees = Meeting_attendees(
                    meeting_id = meetings_sch.id,
                    user_id = user
                )

                meeting_attendees.save()

        return redirect("/"+ current_user_url(request.session["user_id"]) + "/meeting/schedule/"+contact_id)
    return render(request, template, data_dict)  

#*******************************************************************************
# MEETING OPERATIONS SAVE
#*******************************************************************************
@user_access_check     
@login_required
def save_meeting_opertions(request, usertype = None,):
    if request.is_ajax():

        

        return HttpResponse(1)
        




