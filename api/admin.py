from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(City)
admin.site.register(ServiceProvider)
admin.site.register(ServiceType)
admin.site.register(Area)
admin.site.register(Customer)
admin.site.register(Booking)
admin.site.register(ProblemSubCategory)
admin.site.register(SubCategoryBooking)
