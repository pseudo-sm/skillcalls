from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
from django.contrib import auth
# Create your views here.

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

    types = request.GET.get("types")
    types = json.loads(types)
    service_providers = ServiceProvider.objects.all()
    result = []
    for type in types:
        this_type = ServiceType.objects.filter(name=type).first()
        service_providers = service_providers | service_providers.filter(type=this_type)
    
    return JsonResponse(list(service_providers.values()),safe=False)