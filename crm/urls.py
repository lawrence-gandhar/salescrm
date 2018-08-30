from . import views

try:
    from django.urls import path, re_path

    urlpatterns = [
        path('', views.index, name='index'),    
        path('dashboard/', views.dashboard, name='dashboard'),    
    ]

except ImportError:
    from django.conf.urls import url

    urlpatterns = [
        url('', views.index, name='index'),    
        url('dashboard/', views.dashboard, name='dashboard'),    
    ]
