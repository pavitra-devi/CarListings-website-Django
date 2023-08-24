from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from localflavor.in_.models import INStateField #,INZipCodeField

from.utils import user_directory_path

class Location(models.Model):
    address_1 = models.CharField(max_length=200,blank=True)
    address_2 = models.CharField(max_length=200,blank=True)
    city = models.CharField(max_length=64)
    state = INStateField()
    #zip_code = models.CharField(max_length=6,blank=True)

    def __str__(self):
        return f'Location {self.id}'

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path,null=True)
    bio = models.CharField(max_length=200,blank=True)
    phone_number=models.CharField(max_length=12,blank=True)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'
