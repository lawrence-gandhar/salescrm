from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

try:
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('crm.urls'))
    ]
except ImportError:
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^',include('crm.urls')),
    ]

admin.site.site_header = _("TSM CRM - Administration")
admin.site.site_title = _("TSM CRM")