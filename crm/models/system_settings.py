from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.conf import settings


class Dashboard_Settings(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True, blank = True,)
    counters = models.BooleanField(default = True, db_index = True,)
    line_charts = models.BooleanField(default = True, db_index = True,)
    bar_graphs = models.BooleanField(default = True, db_index = True,)
    geo_graph = models.BooleanField(default = True, db_index = True,)
    geo_list = models.BooleanField(default = True, db_index = True,)
    geo_list_filters = models.BooleanField(default = True, db_index = True,)

    class Meta:
        db_table = 'dashboard_settings'
    
    