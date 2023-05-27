from django.db import models
from django.contrib.auth.models import AbstractUser
from .auth_manager import UserManager
from django.utils.translation import gettext_lazy as _
import uuid
import geopy.distance
from django.core.validators import int_list_validator
from . import routes
import numpy as np
import datetime
# Create your models here.

class User(AbstractUser):
    id = models.IntegerField(primary_key=True, unique=True)
    
    username = None
    email = models.EmailField(_("email address"), unique=True)
    
    gender = models.CharField(max_length=1, choices=(
        ("M", "Male"),
        ("F", "Female"),
        ("D", "Else"),
    ))
    
    adress = models.CharField(max_length=500)
    
    points = models.IntegerField(default=0)
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    company = models.ForeignKey("Company", on_delete=models.CASCADE, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __sub__(self, other):
        a = (self.latitude, self.longitude)
        b = (other.latitude, other.longitude)
    
        return geopy.distance.geodesic(a, b).km

    def __str__(self):
        return self.email
    

class Company(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    
    name = models.CharField(max_length=100)
    
    adress = models.CharField(max_length=500)
    
    hub = models.ForeignKey("Hub", on_delete=models.CASCADE)
    
    workload = models.CharField(max_length=2100, validators=(int_list_validator,), default=("0,"*24 + ";")*7)
    
    def __getitem__(self, i):
        d, h = i
        w = self.workload.split(";")
        w = [list(map(int, i.split(",", 23))) for i in w]
        
        return w[d][h]
        
    def __str__(self):
        return self.name
    
    def n_employees(self):
        return len(User.objects.filter(company=self))
    
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        

class Hub(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    latitude = models.FloatField()
    longitude = models.FloatField()

    info = models.CharField(max_length=100, blank=True, default="")

    def __sub__(self, other):
        a = (self.latitude, self.longitude)
        b = (other.latitude, other.longitude)

        return geopy.distance.geodesic(a, b).km
    
    def __floordiv__(self, other):
        a1, a2 = (self.latitude, self.longitude)
        b1, b2 = (other.latitude, other.longitude)
        
        return (a1+a2)/2, (b1+b2)/2
    
    def get_vector(self, other):
        lat1, lon1 = self.latitude, self.longitude  #source
        lat2, lon2 = other.latitude, other.longitude#destination

        return np.array([lat2-lat1, lon2-lon1])



    
class Ride(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="driver")
    
    source_hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name="source")
    
    destination_time = models.DateTimeField(default=datetime.datetime.now)
    
    destination_hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name="destinaiton")
    
    passengers = models.ManyToManyField(User, through="Ride2Passengers")
    
    is_full = models.BooleanField(default=False)

    points = models.IntegerField(default=0)
    
    def get_duration(self, additional=None):
        sources = [i.source_hub for i in self.passengers.all()]
        sources.append(self.source_hub)
        if additional is not None:
            sources.append(additional)
        return routes.get_route_duration(sources, self.destination_hub)
    
    def get_vector(self):
        lat1, lon1 = self.source_hub.latitude, self.source_hub.longitude
        lat2, lon2 = self.destination_hub.latitude, self.destination_hub.longitude
        
        return np.array([lat2-lat1, lon2-lon1])
    
class Ride2Passengers(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    source_hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Ride2Passengers"
        verbose_name_plural = "Rides2Passengers"
    
    
    
