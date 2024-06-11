"""kolomna_museums URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from first import views

urlpatterns = [
    path('main/', admin.site.urls),
    path('', views.main_clients_page),
    path('admin/', views.main_admins_page),
    path('basket/', views.basket_page),
    path('contacts/', views.contacts_page),
    path('museum_info/', views.museum_info_page),
    path('timetable_client/', views.timetable_client_page),
    path('one_reserv/', views.one_reserv_page),
    path('basket_reserv/', views.basket_reserv_page),
    path('museum/', views.museum_page),
    path('all_museums/', views.all_museums_page)
]
