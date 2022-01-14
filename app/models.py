from argparse import _SubParsersAction


import datetime
datetime.datetime.now()
from django.db import models

# Create your models here.


from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# from cloudinary.models import CloudinaryField
from datetime import date, datetime as dt
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
# Create your models here.

class User(AbstractUser):
    role_choices = (('is_admin','Admin'),('is_partner','Partner'),('is_volunteer','Volunteer'))
    role = models.CharField(max_length=20, choices=role_choices,null=False)
    phone = models.IntegerField(blank=False,default=0) 


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True),
    def __str__(self):
        return self.user.username

class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True),
    def __str__(self):
        return self.user.username

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True),
    def __str__(self):
        return self.user.username        


class Contact(models.Model):
   
    name = models.CharField(max_length=60, blank=True)
    email = models.CharField(max_length=60, blank=True)
    subject = models.CharField(max_length=60, blank=True)
    message = models.CharField(max_length=300, blank=True)
    

    def __str__(self):
        return f'{self.user.username}'        


class PartnerInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, blank=True)
    subject = models.CharField(max_length=60, blank=True)
    message = models.CharField(max_length=300, blank=True)
    date = models.DateField(null=True)


 
class VolunteerInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, blank=True)
    subject = models.CharField(max_length=60, blank=True)
    message = models.CharField(max_length=300, blank=True)
    date = models.DateField(null=True)

class Announcement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    subject = models.TextField(max_length=255, default="Add Subject", blank=True)
    information = models.CharField(max_length=60,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=60,blank=True)
   

