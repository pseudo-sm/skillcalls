from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import datetime

class City(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Area(models.Model):

    id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE,verbose_name=("city"))
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        

class ServiceType(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class ServiceProvider(User):

    type = models.ForeignKey(ServiceType, verbose_name=("type"), on_delete=models.CASCADE)
    aadhar_number = models.CharField(unique=True, max_length=100)
    gender = models.CharField(max_length=10)
    father_name = models.CharField(max_length=200)
    mother_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    parent_mobile = models.CharField(max_length=100)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    marital_status = models.CharField(max_length=100)
    school_education = models.CharField(max_length=200)
    technical_education = models.CharField(max_length=200)
    technical_education_domain = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.ForeignKey(City,on_delete=models.CASCADE,verbose_name=("city"))
    area = models.ForeignKey(Area,on_delete=models.CASCADE,verbose_name=("area"))
    address = models.TextField(max_length=100)
    religion = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Service Provider"
        verbose_name_plural = "Service Providers"
    
    def __str__(self):
        return self.get_full_name()

class Customer(User):

    phone = models.CharField(max_length=20)
    address = models.TextField()
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.get_full_name()
    