from email.policy import default
from faulthandler import is_enabled
from django.db import models

# Create your models here.

class ClickverseUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100,blank=False,unique=True)
    password = models.CharField(max_length=100,blank=False)
    # first_name =  models.CharField(max_length=100,blank=False)
    # last_name = models.CharField(max_length=100,blank=False)
    email = models.EmailField(max_length = 70, blank = True,unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default = False)
    is_super_user = models.BooleanField(default=False)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class ClickverseUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_name = models.CharField(max_length=100)
    teamleads_user_id = models.IntegerField()
    is_enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return self.group_name


class UserHasGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.IntegerField(unique=True)
    user_id = models.IntegerField()
    is_enabled = models.BooleanField(default=False)
