from django.contrib import admin
from .models import City,ServiceType,ServiceProvider,Area,Customer
# Register your models here.
admin.site.register(City)
admin.site.register(ServiceProvider)
admin.site.register(ServiceType)
admin.site.register(Area)
admin.site.register(Customer)