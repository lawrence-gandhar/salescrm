from __future__ import unicode_literals
from django.db import models
from crm.models import *
import datetime
from django.contrib.auth.models import User

class Contacts(models.Model):
    company_name = models.CharField(max_length = 250, blank = True, null = True, db_index = True,)
    contact_title = models.CharField(max_length = 10, db_index = True, null = True, blank = True, )
    contact_person = models.CharField(max_length = 250, blank = True, null = True, db_index = True, )
    job_title = models.CharField(max_length = 250, blank = True, null = True, )
    address = models.TextField(blank = True, null = True, )
    contact_phone = models.CharField(max_length = 250, blank = True, null = True, )
    contact_email = models.CharField(max_length = 250, blank = True, null = True, )
    contact_website = models.CharField(max_length = 250, blank = True, null = True, )
    comment = models.TextField(null = True, blank = True, )
    created_on = models.DateTimeField(auto_now_add = True, auto_now = False, db_index = True, null = True, blank = True, )

    class Meta:
        db_table = 'contacts'
        verbose_name_plural = 'Contacts Table'

    def __str__(self):
        return self.company_name.upper()

    def contact_person_name(self):
        return self.contact_title+" "+self.contact_person.title()
        
    def job_title_name(self):
        return self.job_title.title()


class Contacts_meeting(models.Model):
    contact = models.ForeignKey('Contacts', db_index = True, null = True, on_delete = models.SET_NULL, )
    scheduled_by = models.ForeignKey(User, db_index = True, null = True, on_delete = models.SET_NULL, )
    meeting_schedule = models.DateTimeField(db_index = True, null = True, blank = True, )
    agenda = models.TextField(null = True, blank = True,)
    meeting_cancelled = models.BooleanField(default = False, db_index = True,)
    meeting_postponed = models.BooleanField(default = False, db_index = True, )
    meeting_adjourned = models.BooleanField(default = False, db_index = True, )
    created_on = models.DateTimeField(auto_now_add = True, auto_now = False, db_index = True, null = True, blank = True, )
    
    class Meta:
        db_table = 'contacts_meeting_schedule'
        verbose_name_plural = 'Contacts Meeting Schedule'


class Meeting_attendees(models.Model):
    meeting = models.ForeignKey('Contacts_meeting', null = True, db_index = True, blank = True, on_delete = models.CASCADE, )
    user = models.ForeignKey(User, db_index = True, null = True, on_delete = models.SET_NULL, )
    created_on = models.DateTimeField(auto_now_add = True, auto_now = False, db_index = True, null = True, blank = True, )

    class Meta:
        db_table = 'meeting_attendees'
        verbose_name_plural = 'Meeting Attendees List'


class Meeting_logs(models.Model): 
    meeting = models.ForeignKey('Contacts_meeting', null = True, db_index = True, blank = True, on_delete = models.CASCADE, )
    user = models.ForeignKey(User, db_index = True, null = True, on_delete = models.SET_NULL, )   
    log = models.TextField(null = True, blank = True, )    
    created_on = models.DateTimeField(auto_now_add = True, auto_now = False, db_index = True, null = True, blank = True, )     

    class Meta:
        db_table = 'meeting_logs'
        verbose_name_plural = 'Meeting Logs'


class Cancelled_meetings(models.Model):
    meeting = models.ForeignKey('Contacts_meeting', null = True, db_index = True, blank = True, on_delete = models.CASCADE, )
    user = models.ForeignKey(User, db_index = True, null = True, on_delete = models.SET_NULL, )    
    reason = models.TextField(blank = True, null = True,)
    reschedule = models.BooleanField(db_index = True, default = False,)
    created_on = models.DateTimeField(auto_now_add = True, auto_now = False, db_index = True, null = True, blank = True, )     

    class Meta:
        db_table = 'cancelled_meetings'
        verbose_name_plural = 'Cancelled Meetings'


class Postponed_meetings(models.Model):    
    meeting = models.ForeignKey('Contacts_meeting', null = True, db_index = True, blank = True, on_delete = models.CASCADE, )
    user = models.ForeignKey(User, db_index = True, null = True, on_delete = models.SET_NULL, )    
    reason = models.TextField(blank = True, null = True, )
    postponed_to_date = models.DateField(db_index = True, null = True, blank = True, )     
    created_on = models.DateTimeField(auto_now_add = True, auto_now = False, db_index = True, null = True, blank = True, )     

    class Meta:
        db_table = 'postponed_meetings'
        verbose_name_plural = 'Postponed Meetings'


class Adjourned_meetings(models.Model):    
    meeting = models.ForeignKey('Contacts_meeting', null = True, db_index = True, blank = True, on_delete = models.CASCADE, )
    user = models.ForeignKey(User, db_index = True, null = True, on_delete = models.SET_NULL, )    
    reason = models.TextField(blank = True, null = True, )
    adjourned_to_date = models.DateTimeField(db_index = True, null = True, blank = True, )     
    created_on = models.DateTimeField(auto_now_add = True, auto_now = False, db_index = True, null = True, blank = True, )     

    class Meta:
        db_table = 'adjourned_meetings'
        verbose_name_plural = 'Adjourned Meetings'


class Rescheduled_meetings(models.Model):
    meeting = models.ForeignKey('Contacts_meeting', null = True, db_index = True, blank = True, on_delete = models.CASCADE, )
    user = models.ForeignKey(User, db_index = True, null = True, on_delete = models.SET_NULL, )    
    rescheduled_to = models.DateTimeField(db_index = True, null = True, blank = True, )     
    created_on = models.DateTimeField(auto_now_add = True, auto_now = False, db_index = True, null = True, blank = True, )     

    class Meta:
        db_table = 'rescheduled_meetings'
        verbose_name_plural = 'rescheduled Meetings'