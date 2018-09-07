from . import views

try:
    from django.urls import path, re_path

    urlpatterns = [
        path('', views.index, name='index'),    
        re_path(r'^(?P<usertype>[\w.@+-]+)/dashboard/$', views.dashboard, name = 'dashboard'),  
        re_path(r'^(?P<usertype>[\w.@+-]+)/logout/$', views.user_logout, name = 'logout'),     
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/add/$', views.add_lead, name = 'add-lead'),    
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/add-lead-step2/(?P<id>[\d]+)/$', views.add_lead_step_2, name = 'add-lead-step2'),     
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/manage/', views.manage_leads, name = 'manage-leads'),
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/edit-lead-step2/(?P<id>[\d]+)/$', views.add_lead_step_2, name = 'edit-lead-step2'),     
        re_path(r'^(?P<usertype>[\w.@+-]+)/leads/fetch-lead-details/$', views.fetch_lead_details, name = 'fetch-lead-details'),     
    ]

except ImportError:
    from django.conf.urls import url

    urlpatterns = [
        url('', views.index, name='index'),    
        url(r'^(?P<usertype>[\w.@+-]+)/dashboard/$', views.dashboard, name = 'dashboard'),    
        url(r'^(?P<usertype>[\w.@+-]+)/logout/$', views.user_logout, name = 'logout'),    
        url(r'^(?P<usertype>[\w.@+-]+)/leads/add/$', views.add_lead, name = 'add-lead'),    
        url(r'^(?P<usertype>[\w.@+-]+)/leads/add-lead-step2/(?P<id>[\d]+)/$', views.add_lead_step_2, name = 'add-lead-step2'),    
        url(r'^(?P<usertype>[\w.@+-]+)/leads/manage/', views.manage_leads, name = 'manage-leads'),    
        url(r'^(?P<usertype>[\w.@+-]+)/leads/edit-lead-step2/(?P<id>[\d]+)/$', views.add_lead_step_2, name = 'edit-lead-step2'),     
        url(r'^(?P<usertype>[\w.@+-]+)/leads/fetch-lead-details/$', views.fetch_lead_details, name = 'fetch-lead-details'),     
    ]
