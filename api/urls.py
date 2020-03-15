"""skillcalls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('signup-service-provider/',views.create_service_provider,name="create_service_provider"),
    path('get-service-providers/',views.get_service_providers,name="get_service_providers"),
    path('signup-customer/',views.create_customer,name="create_customer"),
    path('customer-login/',views.customer_login,name="customer_login"),
    path('service-provider-login/',views.service_provider_login,name="service_provider_login"),
    path('book-service/',views.book_service,name="book_service"),
    path('fetch-services/',views.fetch_services,name="fetch_services"),
    path('get-service-profile/',views.get_service_profile,name="get_service_profile"),
    path('toggle-status/',views.toggle_status,name="toggle_status"),
    path('set-location/',views.set_location,name="set_location"),
    path('find-nearest/',views.find_nearest,name="find_nearest"),
    path('get-sub-categories/',views.get_sub_categories,name="get_sub_categories"),
    path('get-active-bookings/',views.get_active_bookings,name="get_active_bookings"),
    path('react-booking/',views.react_booking,name="react_booking"),
    path('recur-checking/',views.recur_checking,name="recur_checking"),
    path('fetch-accepted-provider/',views.fetch_accepted_provider,name="fetch_accepted_provider"),
    path('get-booking-location/',views.get_booking_location,name="get_booking_location"),
]

from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
