from datetime import datetime
from datetime import date

from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random

from first.models import UserInfo, Programm, Place, Registr, Favorite

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

# Create your views here.

def registration(request):
    error = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user_info = UserInfo(
                user = User.objects.all().last(),
                gmail = request.POST.get("gmail"),
                telephone = request.POST.get("telephone"),
            )
            user_info.save()
            return redirect('/login')
        else:
            error = 'Пароль не соответствует требованиям.'
    else:
        form = UserCreationForm()

    return render(request, 'registration/sign_up.html', {'form': form, 'error': error})

# def login

def map_page(request):
    if request.method == 'POST':
        user_text = request.POST.get('user_text', '')

    else:
        user_text = None
    context = {
        "user_text": user_text
    }
    return render(request, 'map.html', context)

def main_clients_page(request):
    places = Place.objects.filter()
    context = {
        "places": places,
    }
    return render(request, "main_clients.html", context)

def change_time(i):
    now_weekday = datetime.now().isoweekday()
    now_month = date.today().month
    now_day = date.today().day
    now_hour = datetime.now().hour + 3
    now_minute = datetime.now().minute
    if i.month_start < now_month or (i.month_start == now_month and i.day_start < now_day) or (i.month_start == now_month and i.day_start == now_day and i.hour_start < now_hour) or (i.month_start == now_month and i.day_start == now_day and i.hour_start == now_hour and i.minute_start < now_minute):
        if i.periodicity % 1 == 0:
            i.hour_start += i.periodicity
            if i.hour_start >= 24:
                i.day_start += i.hour_start // 24
                i.hour_start %= 24
                if i.month_start == 2:
                    now_year = datetime.now().year
                    if now_year % 4 == 0:
                        if now_year % 100 == 0 and now_year % 400 == 0:
                            if i.day_start > 29:
                                i.month_start += i.day_start // 29
                                i.day_start %= 29
                        else:
                            if i.day_start > 28:
                                i.month_start += i.day_start // 28
                                i.day_start %= 28
                    else:
                        if i.day_start > 28:
                            i.month_start += i.day_start // 28
                            i.day_start %= 28

                elif i.month_start == 1 or i.month_start == 3 or i.month_start == 5 or i.month_start == 7 or i.month_start == 8 or i.month_start == 10 or i.month_start == 12:
                    if i.day_start > 31:
                        if i.month_start == 12:
                            i.month_start += (i.day_start // 31)
                            i.month_start %= 12
                            i.day_start %= 31
                        else:
                            i.month_start += (i.day_start // 31)
                            i.day_start %= 31
                elif i.month_start == 4 or i.month_start == 6 or i.month_start == 9 or i.month_start == 11:
                    if i.day_start > 30:
                            i.month_start += (i.day_start // 30)
                            i.day_start %= 30
        else:
            d_hour = i.periodicity - i.periodicity % 1
            d_min = i.periodicity % 1
            i.hour_start += d_hour
            i.minute_start += d_min
            if i.minute_start >= 60:
                i.hour_start += i.minute_start // 60
                i.minute_start %= 60
            if i.hour_start >= 24:
                i.day_start += i.hour_start // 24
                i.hour_start %= 24
                if i.month_start == 2:
                    now_year = datetime.now().year
                    if now_year % 4 == 0:
                        if now_year % 100 == 0 and now_year % 400 == 0:
                            if i.day_start > 29:
                                i.month_start += i.day_start // 29
                                i.day_start %= 29
                        else:
                            if i.day_start > 28:
                                i.month_start += i.day_start // 28
                                i.day_start %= 28
                    else:
                        if i.day_start > 28:
                            i.month_start += i.day_start // 28
                            i.day_start %= 28
                elif i.month_start == 1 or i.month_start == 3 or i.month_start == 5 or i.month_start == 7 or i.month_start == 8 or i.month_start == 10 or i.month_start == 12:
                    if i.day_start > 31:
                        if i.month_start == 12:
                            i.month_start += (i.day_start // 31)
                            i.month_start %= 12
                            i.day_start %= 31
                        else:
                            i.month_start += (i.day_start // 31)
                            i.day_start %= 31
                elif i.month_start == 4 or i.month_start == 6 or i.month_start == 9 or i.month_start == 11:
                    if i.day_start > 30:
                        i.month_start += (i.day_start // 30)
                        i.day_start %= 30

@login_required
def basket_page(request):
    user = User.objects.get(username=request.user)
    fv = Favorite.objects.filter(user=user)
    places = []
    for i in fv: places.append(i.place)
    print("PLACES: ", places)
    programms = []
    for j in places:
        for i in Programm.objects.filter(parent=j.id): programms.append(i)
    now_weekday = datetime.now().isoweekday()
    now_month = date.today().month
    now_day = date.today().day
    now_hour = datetime.now().hour + 3
    now_minute = datetime.now().minute
    TIMESWEEK = 168
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    lst = dict()
    k = 0
    for i in days[now_weekday - 1:-1]:
        if now_month == 2:
            now_year = datetime.now().year
            if now_year % 4 == 0:
                if now_year % 100 == 0 and now_year % 400 == 0:
                    if now_day + k > 29:
                        lst[f"{i}, {now_day + k - 29} {months[now_month-1+1]}"] = []
                    else:
                        lst[f"{i}, {now_day + k} {months[now_month-1]}"] = []
                else:
                    if now_day+k > 28:
                        lst[f"{i}, {now_day + k - 28} {months[now_month - 1+1]}"] = []
                    else:
                        lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
            else:
                if now_day + k > 28:
                    lst[f"{i}, {now_day + k - 28} {months[now_month - 1 + 1]}"] = []
                else:
                    lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
        if now_month == 1 or now_month == 3 or now_month == 5 or now_month == 7 or now_month == 8 or now_month == 10 or now_month == 12:
            if now_day + k > 31:
                if now_month == 12:
                    lst[f"{i}, {now_day + k - 31} {months[0]}"] = []
                else:
                    lst[f"{i}, {now_day + k - 31} {months[now_month - 1 + 1]}"] = []
            else:
                lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []

        if now_month == 4 or now_month == 6 or now_month == 9 or now_month == 11:
            if now_day + k > 30:
                lst[f"{i}, {now_day + k - 30} {months[now_month - 1 + 1]}"] = []
            else:
                lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
        k += 1

    for i in days[:now_weekday - 1]:
        if now_month == 2:
            now_year = datetime.now().year
            if now_year % 4 == 0:
                if now_year % 100 == 0 and now_year % 400 == 0:
                    if now_day + k > 29:
                        lst[f"{i}, {now_day + k - 29} {months[now_month - 1 + 1]}"] = []
                    else:
                        lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
                else:
                    if now_day + k > 28:
                        lst[f"{i}, {now_day + k - 28} {months[now_month - 1 + 1]}"] = []
                    else:
                        lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
            else:
                if now_day + k > 28:
                    lst[f"{i}, {now_day + k - 28} {months[now_month - 1 + 1]}"] = []
                else:
                    lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
        if now_month == 1 or now_month == 3 or now_month == 5 or now_month == 7 or now_month == 8 or now_month == 10 or now_month == 12:
            if now_day + k > 31:
                if now_month == 12:
                    lst[f"{i}, {now_day + k - 31} {months[0]}"] = []
                else:
                    lst[f"{i}, {now_day + k - 31} {months[now_month - 1 + 1]}"] = []
            else:
                lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []

        if now_month == 4 or now_month == 6 or now_month == 9 or now_month == 11:
            if now_day + k > 30:
                lst[f"{i}, {now_day + k - 30} {months[now_month - 1 + 1]}"] = []
            else:
                lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
        k += 1
    print(programms)
    for i in programms:
        change_time(i)
        if i.day_start - now_day <= 7:
            lst[list(lst.keys())[i.day_start - now_day]].append([i.name, str(i.hour_start).zfill(2), str(i.minute_start).zfill(2), i.length, i.price_adult])

    for i in lst:
        lst[i] = sorted(lst[i], key=lambda x: x[1])
        lst[i] = sorted(lst[i], key=lambda x: x[2])


    res = []
    for i in lst:
        pr = {
            "day": i,
            "value": []
        }
        for j in lst[i]:
            pr["value"].append({
                "name": j[0],
                "time": f"{j[1]}:{j[2]}",
                "capacity": j[3],
                "price": j[4]
            })
        res.append(pr)
    context = {
        "lst": res
    }

    if request.method == "POST":
        print("done")
        print(request.POST)
        return redirect('/one_revers')
    print(lst)
    return render(request, "basket.html", context)



def contacts_page(request):
    return render(request, "contacts.html")

@login_required
def main_admins_page(request):
    programms = list(Programm.objects.filter())
    now_weekday = datetime.now().isoweekday()
    now_month = date.today().month
    now_day = date.today().day
    now_hour = datetime.now().hour + 3
    now_minute = datetime.now().minute
    TIMESWEEK = 168
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября",
              "декабря"]
    lst = dict()
    k = 0
    for i in days[now_weekday - 1:-1]:
        if now_month == 2:
            now_year = datetime.now().year
            if now_year % 4 == 0:
                if now_year % 100 == 0 and now_year % 400 == 0:
                    if now_day + k > 29:
                        lst[f"{i}, {now_day + k - 29} {months[now_month - 1 + 1]}"] = []
                    else:
                        lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
                else:
                    if now_day + k > 28:
                        lst[f"{i}, {now_day + k - 28} {months[now_month - 1 + 1]}"] = []
                    else:
                        lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
            else:
                if now_day + k > 28:
                    lst[f"{i}, {now_day + k - 28} {months[now_month - 1 + 1]}"] = []
                else:
                    lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
        if now_month == 1 or now_month == 3 or now_month == 5 or now_month == 7 or now_month == 8 or now_month == 10 or now_month == 12:
            if now_day + k > 31:
                if now_month == 12:
                    lst[f"{i}, {now_day + k - 31} {months[0]}"] = []
                else:
                    lst[f"{i}, {now_day + k - 31} {months[now_month - 1 + 1]}"] = []
            else:
                lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []

        if now_month == 4 or now_month == 6 or now_month == 9 or now_month == 11:
            if now_day + k > 30:
                lst[f"{i}, {now_day + k - 30} {months[now_month - 1 + 1]}"] = []
            else:
                lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
        k += 1

    for i in days[:now_weekday - 1]:
        if now_month == 2:
            now_year = datetime.now().year
            if now_year % 4 == 0:
                if now_year % 100 == 0 and now_year % 400 == 0:
                    if now_day + k > 29:
                        lst[f"{i}, {now_day + k - 29} {months[now_month - 1 + 1]}"] = []
                    else:
                        lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
                else:
                    if now_day + k > 28:
                        lst[f"{i}, {now_day + k - 28} {months[now_month - 1 + 1]}"] = []
                    else:
                        lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
            else:
                if now_day + k > 28:
                    lst[f"{i}, {now_day + k - 28} {months[now_month - 1 + 1]}"] = []
                else:
                    lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
        if now_month == 1 or now_month == 3 or now_month == 5 or now_month == 7 or now_month == 8 or now_month == 10 or now_month == 12:
            if now_day + k > 31:
                if now_month == 12:
                    lst[f"{i}, {now_day + k - 31} {months[0]}"] = []
                else:
                    lst[f"{i}, {now_day + k - 31} {months[now_month - 1 + 1]}"] = []
            else:
                lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []

        if now_month == 4 or now_month == 6 or now_month == 9 or now_month == 11:
            if now_day + k > 30:
                lst[f"{i}, {now_day + k - 30} {months[now_month - 1 + 1]}"] = []
            else:
                lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
        k += 1

    for i in programms:
        change_time(i)
        if i.day_start - now_day <= 7:
            lst[list(lst.keys())[i.day_start - now_day]].append(
                [i.name, str(i.hour_start).zfill(2), str(i.minute_start).zfill(2), i.length, i.price_adult])

    for i in lst:
        lst[i] = sorted(lst[i], key=lambda x: x[1])
        lst[i] = sorted(lst[i], key=lambda x: x[2])

    res = []
    for i in lst:
        pr = {
            "day": i,
            "value": []
        }
        for j in lst[i]:
            pr["value"].append({
                "name": j[0],
                "time": f"{j[1]}:{j[2]}",
                "capacity": j[3],
                "price": j[4]
            })
        res.append(pr)
    context = {
        "lst": res
    }

    if request.method == "POST":
        pass

    return render(request, "main_admins.html", context)

@login_required
def museum_info_page(request):
    return render(request, "museum_info.html")

def timetable_client_page(request):
    return render(request, "timetable_client.html")

def one_reserv_page(request):
    return render(request, "one_reserv.html")

def basket_reserv_page(request):
    user = User.objects.get(username=request.user)
    fv = Favorite.objects.filter(user=user)
    places = []
    for i in fv: places.append(i.place)
    programms = []
    for j in places:
        for i in Programm.objects.filter(parent=j.id): programms.append(i)
    now_weekday = datetime.now().isoweekday()
    now_month = date.today().month
    now_day = date.today().day
    now_hour = datetime.now().hour + 3
    now_minute = datetime.now().minute
    TIMESWEEK = 168
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    lst = dict()
    k = 0
    for i in days[now_weekday - 1:-1]:
        if now_month == 2:
            now_year = datetime.now().year
            if now_year % 4 == 0:
                if now_year % 100 == 0 and now_year % 400 == 0:
                    if now_day + k > 29:
                        lst[f"{i}, {now_day + k - 29} {months[now_month-1+1]}"] = []
                    else:
                        lst[f"{i}, {now_day + k} {months[now_month-1]}"] = []
                else:
                    if now_day+k > 28:
                        lst[f"{i}, {now_day + k - 28} {months[now_month - 1+1]}"] = []
                    else:
                        lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
            else:
                if now_day + k > 28:
                    lst[f"{i}, {now_day + k - 28} {months[now_month - 1 + 1]}"] = []
                else:
                    lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
        if now_month == 1 or now_month == 3 or now_month == 5 or now_month == 7 or now_month == 8 or now_month == 10 or now_month == 12:
            if now_day + k > 31:
                if now_month == 12:
                    lst[f"{i}, {now_day + k - 31} {months[0]}"] = []
                else:
                    lst[f"{i}, {now_day + k - 31} {months[now_month - 1 + 1]}"] = []
            else:
                lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []

        if now_month == 4 or now_month == 6 or now_month == 9 or now_month == 11:
            if now_day + k > 30:
                lst[f"{i}, {now_day + k - 30} {months[now_month - 1 + 1]}"] = []
            else:
                lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
        k += 1

    for i in days[:now_weekday - 1]:
        if now_month == 2:
            now_year = datetime.now().year
            if now_year % 4 == 0:
                if now_year % 100 == 0 and now_year % 400 == 0:
                    if now_day + k > 29:
                        lst[f"{i}, {now_day + k - 29} {months[now_month - 1 + 1]}"] = []
                    else:
                        lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
                else:
                    if now_day + k > 28:
                        lst[f"{i}, {now_day + k - 28} {months[now_month - 1 + 1]}"] = []
                    else:
                        lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
            else:
                if now_day + k > 28:
                    lst[f"{i}, {now_day + k - 28} {months[now_month - 1 + 1]}"] = []
                else:
                    lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
        if now_month == 1 or now_month == 3 or now_month == 5 or now_month == 7 or now_month == 8 or now_month == 10 or now_month == 12:
            if now_day + k > 31:
                if now_month == 12:
                    lst[f"{i}, {now_day + k - 31} {months[0]}"] = []
                else:
                    lst[f"{i}, {now_day + k - 31} {months[now_month - 1 + 1]}"] = []
            else:
                lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []

        if now_month == 4 or now_month == 6 or now_month == 9 or now_month == 11:
            if now_day + k > 30:
                lst[f"{i}, {now_day + k - 30} {months[now_month - 1 + 1]}"] = []
            else:
                lst[f"{i}, {now_day + k} {months[now_month - 1]}"] = []
        k += 1

    for i in programms:
        change_time(i)
        if i.day_start - now_day <= 7:
            lst[list(lst.keys())[i.day_start - now_day]].append([i.name, str(i.hour_start).zfill(2), str(i.minute_start).zfill(2), i.length, i.price_adult])

    for i in lst:
        lst[i] = sorted(lst[i], key=lambda x: x[1])
        lst[i] = sorted(lst[i], key=lambda x: x[2])


    res = []
    for i in lst:
        pr = {
            "day": i,
            "value": []
        }
        for j in lst[i]:
            pr["value"].append({
                "name": j[0],
                "time": f"{j[1]}:{j[2]}",
                "capacity": j[3],
                "price": j[4]
            })
        res.append(pr)
    context = {
        "lst": res
    }

    return render(request, "basket_reserv.html", context)

def museum_page(request, id):
    places = Place.objects.filter(id=id)
    context = {
        "places": places[0]
    }
    programms = list(Programm.objects.filter(parent=id))
    context["programm"] = programms
    user = User.objects.get(username=request.user)

    if request.method == "POST":
        fv = Favorite.objects.filter(place=places[0])
        if len(list(fv))> 0:
            fv = fv.filter(user=user)
            if len(list(fv)) > 0:
                pass
            else:
                record = Favorite(
                    place = places[0],
                    user=user
                )
                record.save()
        else:
            record = Favorite(
                place=places[0],
                user=user
            )
            record.save()

    return render(request, "museum.html", context)


def all_museums_page(request):
    return render(request, "all_museums.html")

def upload_place_page(request):
    def init_image():
        try:
            message = request.FILES
            print(message)
            image = message['image_custom']
        except:
            return None
        else:
            return image

    context = {
        'success': 0
    }
    if request.method == "POST":
        record = Place(
            name=request.POST.get("name"),
            place=request.POST.get("place"),
            image=init_image(),
            description=request.POST.get("description", ""),
        )
        record.save()
        context['success'] = 1

    return render(request, 'upload_place.html', context)


def upload_programm_page(request):
    context = {
        'success': 0
    }

    if request.method == "POST":
        start = list(map(str, str(request.POST.get("start")).split()))
        try:
            time = list(map(int, start[0].split(":")))
            print(time)
            date = list(map(int, start[1].split(".")))
        except:
            time = [0, 0]
            date = [0, 0]
        place = request.POST.get("place")
        parent_id = Place.objects.filter(name=place)
        parent_id = parent_id[0].id
        record = Programm(
            name=request.POST.get("name"),
            length = int(request.POST.get("length")),
            month_start = date[1],
            day_start = date[0],
            hour_start = time[0],
            minute_start = time[1],
            periodicity = request.POST.get("periodicity"),
            capacity = request.POST.get("capacity"),
            price_adult = request.POST.get("price_adult"),
            price_children = request.POST.get("price_children"),
            price_invalid = request.POST.get("price_invalid"),
            discount_price_adult = request.POST.get("discount_price_adult"),
            discount_price_invalid = request.POST.get("discount_price_invalid"),
            discount_price_children = request.POST.get("discount_price_children"),
            parent = parent_id
        )
        record.save()
        context['success'] = 1

    return render(request, 'upload_programm.html', context)
