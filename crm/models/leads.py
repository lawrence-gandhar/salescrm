from __future__ import unicode_literals
from django.db import models
from crm.models import *

#************************************************************************************************************
# Lead Table
#************************************************************************************************************

class Leads_tbl(models.Model):

	company_name = models.CharField(db_index = True, max_length = 250,)
	contact_title = models.CharField(db_index = True, max_length = 3,)
	contact_firstname = models.CharField(db_index = True, max_length = 50,)
	contact_lastname = models.CharField(db_index = True, max_length = 50,)
	contact_details = models.TextField(blank = True,)
	contact_designation = models.CharField(max_length = 50, blank = True,)
	address = models.TextField(blank = True,)
	country = models.CharField(max_length = 50, blank = True, db_index = True,)
	phone = models.CharField(max_length = 20, blank = True,)
	extension = models.CharField(max_length = 10, blank = True,)
	fax = models.CharField(max_length = 20, blank = True,)
	email = models.EmailField(max_length = 250, blank = True, db_index = True,)
	website = models.CharField(max_length = 200, blank = True, db_index = True,)
	lead_type = models.ForeignKey('Lead_type', on_delete = models.SET_NULL, null = True, blank = True, db_index = True,)
	assigned_to = models.IntegerField(db_index = True, default = 0,)
	status = models.ForeignKey('Lead_status',default = 1, on_delete = models.SET_NULL, null = True, blank = True, db_index = True,)
	line_of_business = models.ForeignKey('Lead_line_of_business', on_delete = models.SET_NULL, null = True, blank = True, db_index = True,)
	payment_type = models.ForeignKey('Lead_payment_type', on_delete = models.SET_NULL, null = True, blank = True, db_index = True,)
	probability = models.ForeignKey('Lead_probability', on_delete = models.SET_NULL, null = True, blank = True, db_index = True,)
	fte = models.CharField(max_length = 20, blank = True,)
	annual = models.CharField(max_length = 20, blank = True,)
	active = models.BooleanField(default = True, db_index = True,)
	creation_date = models.DateTimeField(auto_now_add = True,auto_now = False, db_index = True,)
	last_updated = models.DateTimeField(auto_now_add = False,auto_now = True, db_index = True,)
	
	def __str__(self):
		return self.company_name
	
	class Meta:	
		db_table = 'leads_tbl'
		ordering = ['pk']
		verbose_name_plural = 'Leads Table'
		
#************************************************************************************************************
# Lead Type Table
#************************************************************************************************************

class Lead_type(models.Model):

	name = models.CharField(db_index = True, max_length = 100, unique = True,)
	active = models.BooleanField(db_index = True, default = True,)
	creation_date = models.DateTimeField(auto_now_add = True,auto_now = False, db_index = True,)
	last_updated = models.DateTimeField(auto_now_add = False,auto_now = True, db_index = True,)
	
	def __str__(self):
		return self.name
	
	class Meta:	
		db_table = 'lead_type'
		ordering = ['pk']
		verbose_name_plural = 'Leads Type Table'

		
#************************************************************************************************************
# Lead Type Table
#************************************************************************************************************		
	

class Lead_status(models.Model):
	
	name = models.CharField(db_index = True, max_length = 100,unique = True,)
	active = models.BooleanField(db_index = True, default = True,)
	creation_date = models.DateTimeField(auto_now_add = True,auto_now = False, db_index = True,)
	last_updated = models.DateTimeField(auto_now_add = False,auto_now = True, db_index = True,)
	
	def __str__(self):
		return self.name
	
	class Meta:	
		db_table = 'lead_status'
		ordering = ['pk']
		verbose_name_plural = 'Lead Status Table'
	
		
#************************************************************************************************************
# Lead - Line Of Business  Table
#************************************************************************************************************

class Lead_line_of_business(models.Model):
	
	name = models.CharField(db_index = True, max_length = 150,unique = True,)
	active = models.BooleanField(db_index = True, default = True,)
	creation_date = models.DateTimeField(auto_now_add = True,auto_now = False, db_index = True,)
	last_updated = models.DateTimeField(auto_now_add = False,auto_now = True, db_index = True,)
	
	def __str__(self):
		return self.name
	
	class Meta:	
		db_table = 'lead_line_of_business'
		ordering = ['pk']
		verbose_name_plural = 'Leads Line Of Business Table'
	
#************************************************************************************************************
# Lead - Payment Type Table
#************************************************************************************************************

class Lead_payment_type(models.Model):
	
	name = models.CharField(db_index = True, max_length = 150,unique = True,)
	active = models.BooleanField(db_index = True, default = True,)
	creation_date = models.DateTimeField(auto_now_add = True,auto_now = False, db_index = True,)
	last_updated = models.DateTimeField(auto_now_add = False,auto_now = True, db_index = True,)
	
	def __str__(self):
		return self.name
	
	class Meta:	
		db_table = 'lead_payment_type'
		ordering = ['pk']
		verbose_name_plural = 'Leads Payment Type Table'

	
#************************************************************************************************************
# Lead - Probability Table
#************************************************************************************************************	

class Lead_probability(models.Model):
	
	name = models.CharField(db_index = True, max_length = 150,unique = True,)
	active = models.BooleanField(db_index = True, default = True,)
	creation_date = models.DateTimeField(auto_now_add = True,auto_now = False, db_index = True,)
	last_updated = models.DateTimeField(auto_now_add = False,auto_now = True, db_index = True,)
	
	def __str__(self):
		return self.name
	
	class Meta:	
		db_table = 'lead_probability'
		ordering = ['pk']
		verbose_name_plural = 'Leads Probability Table'
		
		
	
#************************************************************************************************************
# Lead - Program Requirement Table
#************************************************************************************************************	

class Lead_program_requirement(models.Model):
	
	name = models.CharField(db_index = True, max_length = 150,unique = True,)
	active = models.BooleanField(db_index = True, default = True,)
	creation_date = models.DateTimeField(auto_now_add = True,auto_now = False, db_index = True,)
	last_updated = models.DateTimeField(auto_now_add = False,auto_now = True, db_index = True,)
	
	def __str__(self):
		return self.name
	
	class Meta:	
		db_table = 'lead_program_requirement'
		ordering = ['pk']
		verbose_name_plural = 'Leads Program Requirement Table'
		
		
#************************************************************************************************************
# Lead - Call Purpose Table
#************************************************************************************************************	

class Lead_call_purpose(models.Model):
	
	name = models.CharField(db_index = True, max_length = 150,unique = True,)
	active = models.BooleanField(db_index = True, default = True,)
	creation_date = models.DateTimeField(auto_now_add = True,auto_now = False, db_index = True,)
	last_updated = models.DateTimeField(auto_now_add = False,auto_now = True, db_index = True,)
	
	def __str__(self):
		return self.name
	
	class Meta:	
		db_table = 'lead_call_purpose'
		ordering = ['pk']
		verbose_name_plural = 'Leads Call Purpose Table'
			

#************************************************************************************************************
# Lead - Pricing Model Table
#************************************************************************************************************	

class Lead_pricing_model(models.Model):
	
	name = models.CharField(db_index = True, max_length = 150,unique = True,)
	active = models.BooleanField(db_index = True, default = True,)
	creation_date = models.DateTimeField(auto_now_add = True,auto_now = False, db_index = True,)
	last_updated = models.DateTimeField(auto_now_add = False,auto_now = True, db_index = True,)
	
	def __str__(self):
		return self.name
	
	class Meta:	
		db_table = 'lead_pricing_model'
		ordering = ['pk']
		verbose_name_plural = 'Leads Pricing Model Table'		


#************************************************************************************************************
# Lead Questionnaire - Table
#************************************************************************************************************			

class Lead_questionnaire_model(models.Model):	

    lead = models.OneToOneField('Leads_tbl', unique=True, db_index = True, on_delete = models.CASCADE)
    qpr = models.TextField(blank= True,)
    lcp = models.TextField(blank= True,)
    lpm = models.TextField(blank= True,)
    inbound_per_month = models.IntegerField(default = 0, db_index = True, null = True, blank = True,)
    outbound_per_month = models.IntegerField(default = 0, db_index = True, null = True, blank = True,)
    inbound_mins_per_call = models.IntegerField(default = 0, db_index = True, null = True, blank = True,)
    outbound_mins_per_call = models.IntegerField(default = 0, db_index = True, null = True, blank = True,)
    call_contact = models.CharField(blank = True,max_length = 20,)
    anticipated_date = models.CharField(blank = True,max_length = 20,)
    product_service_description = models.TextField(blank = True,)
    area_of_operation = models.TextField(blank = True, max_length = 100,)
    work_hours = models.FloatField(default = 0, db_index = True, null = True, blank = True,)
    centers_interested = models.TextField(blank = True,)
    pricing = models.FloatField(default = 0, db_index = True, null = True, blank = True,)
    comments = models.TextField(blank = True,)
    creation_date = models.DateTimeField(auto_now_add = True,auto_now = False, db_index = True,)
    last_updated = models.DateTimeField(auto_now_add = False,auto_now = True, db_index = True,)	

    def __str__(self):
        return self.creation_date
	
    class Meta:	
        db_table = 'lead_questionnaire_model'
        ordering = ['pk']
        verbose_name_plural = 'Leads Questionnaire Model Table'	
		