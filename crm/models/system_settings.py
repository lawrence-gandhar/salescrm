from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.conf import settings
from crm.models import *


class Dashboard_Settings(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True, blank = True,)
    counters = models.BooleanField(default = True, db_index = True,)
    polar_area = models.BooleanField(default = True, db_index = True,)
    line_charts = models.BooleanField(default = True, db_index = True,)
    bar_graphs = models.BooleanField(default = False, db_index = True,)
    geo_graph = models.BooleanField(default = False, db_index = True,)
    geo_list = models.BooleanField(default = False, db_index = True,)
    geo_list_filters = models.BooleanField(default = False, db_index = True,)
    form2_enabled = models.BooleanField(default = False, db_index = True)

    class Meta:
        db_table = 'dashboard_settings'
    

class Counters_Settings(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True, blank = True,)
    counters_customization = models.BooleanField(default = True, db_index = True,)
    lead_status = models.ForeignKey(Lead_status, on_delete = models.SET_NULL, db_index = True, null = True, blank = True,)
    filters = models.BooleanField(db_index = True, default = True,)

    class Meta:
        db_table = 'counters_settings'


class Bargraph_Settings(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True, blank = True,)
    bar_customization = models.BooleanField(default = True, db_index = True,)
    lead_status = models.ForeignKey(Lead_status, on_delete = models.SET_NULL, db_index = True, null = True, blank = True,)
    filters = models.BooleanField(db_index = True, default = True,)
    
    class Meta:
        db_table = 'bargraph_settings'