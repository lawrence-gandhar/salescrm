from . import views

try:
    from django.urls import path, re_path

    urlpatterns = [
        path('', views.index, name='index'),    
    ]

except ImportError:
    from django.conf.urls import url

    urlpatterns = [
        url('', views.index, name='index'),    
    ]
