from . import views
from django.conf import settings
from django.conf.urls.static import static

try:
    from django.urls import path, re_path

    urlpatterns = [
        path('', views.index, name='index'),    
        re_path(r'^(?P<usertype>[\w.@+-]+)/dashboard/$', views.dashboard, name = 'dashboard'),  
        re_path(r'^(?P<usertype>[\w.@+-]+)/logout/$', views.user_logout, name = 'logout'),     
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/add/$', views.add_lead, name = 'add-lead'),    
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/(?P<slug>[\w]+)/(?P<step>[\d])/(?P<id>[\d]+)/$', views.add_lead_step_2,),     
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/manage/', views.manage_leads, name = 'manage-leads'),
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/fetch-lead-details/$', views.fetch_lead_details, name = 'fetch-lead-details'), 
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/timeline/(?P<id>[\d]+)/$', views.timeline), 
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/messages/(?P<id>[\d]+)/$', views.lead_messages),
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/assignments/$', views.lead_assignments,),  
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/edit-assignment/(?P<id>[\d]+)/$', views.lead_assignments_edit),       
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/lead_multiple_status_set/$', views.lead_multiple_status_set),       
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/lead_multiple_active_set/$', views.lead_multiple_active_set),       
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/lead_message_add/$', views.lead_message_add),   
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/stats/$', views.lead_stats),  
        re_path(r'^(?P<usertype>[\w.@+-]+)/documentation/$', views.documentation), 
        re_path(r'^(?P<usertype>[\w.@+-]+)/system_settings/$', views.system_settings), 
        re_path(r'^(?P<usertype>[\w.@+-]+)/dashboard_settings/$', views.dashboard_settings),

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

except ImportError:
    from django.conf.urls import url

    urlpatterns = [
        url('', views.index, name='index'),    
        url(r'^(?P<usertype>[\w.@+-]+)/dashboard/$', views.dashboard, name = 'dashboard'),    
        url(r'^(?P<usertype>[\w.@+-]+)/logout/$', views.user_logout, name = 'logout'),    
        url(r'^(?P<usertype>[\w.@+-]+)/leads/add/$', views.add_lead, name = 'add-lead'),    
        url(r'^(?P<usertype>[\w.@+-]+)/leads/(?P<slug>[\w]+)/(?P<step>[\d])/(?P<id>[\d]+)/$', views.add_lead_step_2,),    
        url(r'^(?P<usertype>[\w.@+-]+)/leads/manage/', views.manage_leads, name = 'manage-leads'),    
        url(r'^(?P<usertype>[\w.@+-]+)/leads/fetch-lead-details/$', views.fetch_lead_details, name = 'fetch-lead-details'),    
        url(r'^(?P<usertype>[\w.@+-]+)/leads/timeline/(?P<id>[\d]+)/$', views.timeline),  
        url(r'^(?P<usertype>[\w.@+-]+)/leads/messages/(?P<id>[\d]+)/$', views.lead_messages),  
        url(r'^(?P<usertype>[\w.@+-]+)/leads/assignments/$', views.lead_assignments,), 
        url(r'^(?P<usertype>[\w.@+-]+)/leads/edit-assignment/(?P<id>[\d]+)/$', views.lead_assignments_edit),    
        url(r'^(?P<usertype>[\w.@+-]+)/leads/lead_multiple_status_set/$', views.lead_multiple_status_set), 
        url(r'^(?P<usertype>[\w.@+-]+)/leads/lead_multiple_active_set/$', views.lead_multiple_active_set), 
        url(r'^(?P<usertype>[\w.@+-]+)/leads/lead_message_add/$', views.lead_message_add),  
        url(r'^(?P<usertype>[\w.@+-]+)/leads/stats/$', views.lead_stats),  
        url(r'^(?P<usertype>[\w.@+-]+)/documentation/$', views.documentation), 
        url(r'^(?P<usertype>[\w.@+-]+)/system_settings/$', views.system_settings),  
        url(r'^(?P<usertype>[\w.@+-]+)/dashboard_settings/$', views.dashboard_settings),  
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
