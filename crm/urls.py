from . import views

try:
    from django.urls import path, re_path

    urlpatterns = [
        path('', views.index, name='index'),    
        re_path(r'^(?P<usertype>[\w.@+-]+)/dashboard/', views.dashboard, name = 'dashboard'),  
        re_path(r'^(?P<usertype>[\w.@+-]+)/logout/', views.user_logout, name = 'logout'),     
    ]

except ImportError:
    from django.conf.urls import url

    urlpatterns = [
        url('', views.index, name='index'),    
        url(r'^(?P<usertype>[\w.@+-]+)/dashboard/', views.dashboard, name = 'dashboard'),    
        url(r'^(?P<usertype>[\w.@+-]+)/logout/', views.user_logout, name = 'logout'),    
    ]
