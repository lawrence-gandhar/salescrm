from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#
# USERTYPE MODEL
#

class Usertypes(models.Model):
    name = models.CharField(max_length = 20, unique = True, db_index = True,)
    sub_link = models.CharField(max_length = 250, unique = True, db_index = True, blank = True, null = True,) 
    menu_template_name = models.CharField(max_length = 100, null = True, blank = True, db_index = True,)
    status = models.BooleanField(default = 1, db_index = True,)

    def __str__(self):
        return self.name.title()

class User_usertype(models.Model):
    user = models.OneToOneField(User, on_delete = models.SET_NULL, db_index = True, null = True, blank = True,)
    usertype = models.OneToOneField(Usertypes, on_delete = models.SET_NULL, db_index = True, null = True, blank = True,)


