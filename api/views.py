from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
import firebase_admin
from firebase_admin import db
# Create your views here.
from firebase_admin import credentials
if (not len(firebase_admin._apps)):
    cred = credentials.Certificate('api/service-account.json') 
    default_app = firebase_admin.initialize_app(cred,{'databaseURL': 'https://skillcallsdb-eaa49.firebaseio.com/'})
db = db.reference()
# print(db.child("test").get())
def listener(event):
    print(event.event_type)  # can be 'put' or 'patch'
    print(event.path)  # relative to the reference, it seems
    print(event.data)  # new data at /reference/event.path. None if deleted
# db.child("service_provider").listen(listener)
def customer_login(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    user = Customer.objects.filter(username=username,password=password).first()
    if user is not None:
        return JsonResponse({"status":True,"auth_id":user.pk})
    else:
        return JsonResponse({'status':False})

def service_provider_login(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    user = ServiceProvider.objects.filter(username=username,password=password).first()
    if user is not None:
        return JsonResponse({"status":True,"auth_id":user.pk})
    else:
        return JsonResponse({'status':False})

def create_service_provider(request):
    first_name = request.GET.get("first_name")
    last_name = request.GET.get("last_name")
    phone = request.GET.get("phone")
    address = request.GET.get("address")
    username = request.GET.get("username")
    password = request.GET.get("password")
    type = request.GET.get("type")
    aadhar_number = request.GET.get("aadhar_number")
    gender = request.GET.get("gender")
    father_name = request.GET.get("father_name")
    mother_name = request.GET.get("mother_name")
    parent_mobile = request.GET.get("parent_mobile")
    dob = request.GET.get("dob")
    marital_status = request.GET.get("marital_status")
    school_education = request.GET.get("school_education")
    technical_education = request.GET.get("technical_education")
    technical_education_domain = request.GET.get("technical_education_domain")
    district = request.GET.get("district")
    city = request.GET.get("city")
    area = request.GET.get("area")
    religion = request.GET.get("religion")
    type = ServiceType.objects.get(name=type)
    city = City.objects.filter(name=city).first()
    # district = District.objects.filter(name=district).first()
    area = Area.objects.filter(name=area).first()
    service_provider = ServiceProvider.objects.create(first_name=first_name,last_name=last_name,mobile=phone,address=address,username=username,password=password,type=type,aadhar_number=aadhar_number,gender=gender,father_name=father_name,mother_name=mother_name,parent_mobile=parent_mobile,dob=dob,marital_status=marital_status,school_education=school_education,technical_education=technical_education,technical_education_domain=technical_education_domain,district=district,area=area,city=city,religion=religion)
    return service_provider_login(request)

def create_customer(request):

    first_name = request.GET.get("first_name")
    last_name = request.GET.get("last_name")
    phone = request.GET.get("phone")
    address = request.GET.get("address")
    username = request.GET.get("username")
    password = request.GET.get("password")
    customer = Customer.objects.create(first_name=first_name,last_name=last_name,phone=phone,address=address,username=username,password=password)
    return customer_login(request)

def get_service_providers(request):

    type = request.GET.get("type")
    service_providers = ServiceProvider.objects.all()
    this_type = ServiceType.objects.filter(id=type).first()
    service_providers = service_providers.filter(city__name="Bhubaneswar")
    service_providers = service_providers | service_providers.filter(type=this_type)
    result = []
    for each in service_providers:
        result.append({"title":this_type.name,"coordinates":{"latitude":float(each.lat),"longitude":float(each.lon)},"image":this_type.image.url})
    return JsonResponse(result,safe=False)

from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

@csrf_exempt
def find_nearest(request):
    media = request.FILES.get("media")
    auth_id = request.POST.get("auth_id")
    city = request.POST.get("city")
    type=request.POST.get("type_id")
    lat = request.POST.get("lat")
    lon = request.POST.get("lon")
    description = request.POST.get("description")
    sub_category = request.POST.get("sub_category_id")
    sub_categories = json.loads(sub_category)
    this_type = ServiceType.objects.get(id=type)
    sub_category_objects = []
    for each in sub_categories:
        this_sub_category = ProblemSubCategory.objects.get(id=each)
        sub_category_objects.append(this_sub_category)

    service_providers = ServiceProvider.objects.filter(city__name=city,type=this_type)
    lat = float(lat)
    lon = float(lon)
    mapped_distance = {}
    for each in service_providers:
        mapped_distance.update({each.id:haversine(lon,lat,float(each.lon),float(each.lat))})  
    distance_list = list(mapped_distance.values())  
    distance_list.sort()
    min = distance_list[0]
    print(min)
    id = (list(mapped_distance.keys())[list(mapped_distance.values()).index(min)])
    nearest = [provider_id for provider_id in mapped_distance if mapped_distance[provider_id]<5]
    return book_service(auth_id,nearest,media,description,sub_category_objects)

def book_service(auth_id,nearest,media,description,sub_category_objects):
    this_customer = Customer.objects.get(id=auth_id)
    booking = Booking(customer=this_customer,media=media,description=description)
    booking.save()
    for each in sub_category_objects:
            scb = SubCategoryBooking(booking=booking,sub_category=each)
            scb.save()
    for each_provider in nearest:
        this_service_provider = ServiceProvider.objects.get(id=each_provider)
        db.child("service_provider").child(str(this_service_provider.id)).update({"booking":booking.id})
        this_service_provider.active_booking = booking.id
        this_service_provider.save()
    return JsonResponse({"booking_id":booking.id},safe=False)

def fetch_services(request):
    service_types = ServiceType.objects.all().values()
    return JsonResponse(list(service_types),safe=False)

def get_service_profile(request):
    id = request.GET.get("id")
    this_provider = ServiceProvider.objects.filter(id=int(id)).values()
    return JsonResponse(list(this_provider),safe=False)

def toggle_status(request):
    id = request.GET.get("id")
    this_provider = ServiceProvider.objects.get(id=id)
    this_provider.active = not(this_provider.active)
    this_provider.save()
    return JsonResponse(this_provider.active,safe=False)

def set_location(request):

    id = request.GET.get("id")
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    this_provider = ServiceProvider.objects.get(id=id)
    this_provider.lat = lat
    this_provider.lon = lon
    this_provider.save()
    return JsonResponse(True,safe=False)

def get_sub_categories(request):
    type = request.GET.get("type_id")
    this_type = ServiceType.objects.get(id=type)
    problem_subcategories = ProblemSubCategory.objects.filter(service_type=this_type)

    return JsonResponse(list(problem_subcategories.values()),safe=False)

def get_active_bookings(request):
    auth_id = request.GET.get("auth_id")
    service_provider = ServiceProvider.objects.get(id=auth_id)
    if service_provider.active_booking is not "-":
        this_booking = list(Booking.objects.filter(id=service_provider.active_booking).values("id","customer__first_name","customer__address","id","customer__phone","media","description","customer__username"))[0]
    else:
        return JsonResponse(False,safe=False)
    print(this_booking)
    subcats = SubCategoryBooking.objects.values_list("sub_category__name").filter(booking=this_booking["id"]) 
    this_booking["sub_categories"] = list(subcats)
    return JsonResponse([this_booking],safe=False)

def react_booking(request):

    minimum_amount = request.GET.get("minimum_amount")
    booking_id = request.GET.get("booking_id")
    auth_id = request.GET.get("auth_id")
    status = request.GET.get("status")
    this_service_provider=ServiceProvider.objects.get(id=auth_id)
    this_booking = Booking.objects.get(id=booking_id)
    if this_booking.status == "0" :
        this_booking.status = status
        this_booking.minimum_amount = minimum_amount
        this_booking.service_provider = this_service_provider
        this_booking.save()
    else:
        this_service_provider.active_booking = "-"
        return JsonResponse({"status":False},safe=False)
    return JsonResponse({"status":True,"booking_id":this_booking.id},safe=False)

def recur_checking(request):
    booking_id = request.GET.get("booking_id")
    this_booking = Booking.objects.get(id=booking_id)
    if this_booking.status == 1:
        return JsonResponse(True,safe=False)
    else:
        return JsonResponse(False,safe=False)

