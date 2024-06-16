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
from django.contrib.auth import views as auth_views

from first import views

urlpatterns = [
    path('main/', admin.site.urls),
    path('', views.main_clients_page),
    path('user/registration/', views.registration),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', auth_views.LogoutView.as_view()),
    path('admin/', views.main_admins_page),
    path('basket/', views.basket_page),
    path('contacts/', views.contacts_page),
    path('museum_info/', views.museum_info_page),
    path('timetable_client/', views.timetable_client_page),
    path('one_reserv/', views.one_reserv_page),
    path('basket_reserv/', views.basket_reserv_page),
    path('museum/<int:id>', views.museum_page),
    path('all_museums/', views.all_museums_page),
    path('upload_place/', views.upload_place_page),
    path('upload_programm/', views.upload_programm_page),
    path('map/', views.map_page),
    path('admin_reserv/', views.admin_reserv_page),
    path('error_count/<str:ids>', views.error_count_page)
]
