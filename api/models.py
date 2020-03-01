from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import datetime
from django.db import models
from django.db.models import signals

def create_customer(sender, instance, created, **kwargs):
    print("action")

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
    image = models.ImageField(upload_to="service_types/",null=True,blank=True)
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
    lat = models.CharField(max_length=100,null=True,blank=True)
    lon = models.CharField(max_length=100,null=True,blank=True)
    active_booking = models.IntegerField(null=True,blank=True)
    class Meta:
        verbose_name = "Service Provider"
        verbose_name_plural = "Service Providers"
    
    def __str__(self):
        return self.get_full_name() + " ( "+str(self.id)+" )"

class Customer(User):

    phone = models.CharField(max_length=20,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers" 

    def __str__(self):
        return self.get_full_name() + " " + str(self.id)

class ProblemSubCategory(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    service_type = models.ForeignKey(ServiceType,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="problem_sub_category")

    def __str__(self):
        return self.name
    

class Booking(models.Model):

    id = models.AutoField(primary_key=True)
    service_provider = models.ForeignKey(ServiceProvider,on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    bill_amount = models.CharField(max_length=200,null=True,blank=True)
    status = models.CharField(max_length=200,default="0")
    media = models.ImageField(upload_to="bookings/",null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    minimum_amount = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return str(self.id)

class SubCategoryBooking(models.Model):

    sub_category = models.ForeignKey(ProblemSubCategory,on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE)

signals.post_save.connect(receiver=create_customer, sender=Customer)
