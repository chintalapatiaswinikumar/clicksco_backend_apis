from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class FollowappUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100,blank=False,unique=True)
    password = models.CharField(max_length=100,blank=False)
    email = models.EmailField(max_length = 70, blank = True,unique=True)
    questions = ArrayField(models.CharField(max_length = 1000),blank = True)
    answers = ArrayField(models.CharField(max_length = 1000),blank = True)
    followers = ArrayField(models.CharField(max_length = 1000),blank = True)
    following = ArrayField(models.CharField(max_length = 1000),blank = True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default = False)
    is_super_user = models.BooleanField(default=False)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.username

