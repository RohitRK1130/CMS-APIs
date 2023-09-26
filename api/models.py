from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from rest_framework.permissions import BasePermission

from .constants import USER_ROLE

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user.role == "1":
                return True
        except:
            pass
        return False

class Categories(models.Model):
    name = models.CharField(max_length=30)

class User(AbstractUser):
    phone = models.CharField(max_length=10)
    address = models.TextField(blank=True)
    city = models.CharField(default="", max_length=255, blank=True)
    state = models.CharField(default="",max_length=255, blank=True)
    country = models.CharField(default="", max_length=255, blank=True)
    pincode = models.CharField(max_length=6)
    role = models.CharField(max_length=1, choices=USER_ROLE)
        
class ContentItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=300)
    summary = models.TextField(max_length=60,blank=True)
    document =  models.FileField(upload_to='api/v1/',default='')
    categories = models.ManyToManyField(Categories)


