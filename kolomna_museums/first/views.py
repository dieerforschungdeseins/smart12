from django.shortcuts import render

# Create your views here.

def main_clients_page(request):
    return render(request, "main_clients.html")

def basket_page(request):
    return render(request, "basket.html")

def contacts_page(request):
    return render(request, "contacts.html")

def main_admins_page(request):
    return render(request, "main_admins.html")


def museum_info_page(request):
    return render(request, "museum_info.html")

def timetable_client_page(request):
    return render(request, "timetable_client.html")

def one_reserv_page(request):
    return render(request, "one_reserv.html")

def basket_reserv_page(request):
    return render(request, "basket_reserv.html")

def museum_page(request):
    return render(request, "museum.html")


def all_museums_page(request):
    return render(request, "all_museums.html")