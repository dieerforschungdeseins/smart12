from datetime import datetime
from datetime import date

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from django.http import HttpResponse

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
            user = User.objects.all().last()
            info = list(UserInfo.objects.filter(user=user))[0]
            if len(info) > 0:
                return redirect("../error_account")
            user_info = UserInfo(
                user = user,
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

def error_account_page(request):
    return render(request, "error_account.html")

def main(request):
    print("..")
    return redirect('../../../../')

def account_page(request):
    user = User.objects.get(username=request.user)
    user_info = list(UserInfo.objects.filter(user=user))[0]
    context = dict()
    context["info"] = user_info
    return render(request, "account.html",  context)


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
    print(days[now_weekday-1:len(days):])
    for i in days[now_weekday-1:len(days):]:
        print(i)
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
        if i.day_start - now_day <= 6:
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
    for i in days[now_weekday - 1:len(days)]:
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
        rgs = Registr.objects.filter(programm_id=i.id)
        adults = 0
        children = 0
        invalid = 0
        for j in list(rgs):
            adults += int(j.adult_count)
            children += int(j.children_count)
            invalid += int(j.invalid_count)

        if i.day_start - now_day <= 6:
            lst[list(lst.keys())[i.day_start - now_day]].append(
                [i.name, str(i.hour_start).zfill(2), str(i.minute_start).zfill(2), i.length, i.price_adult, adults, children, invalid])

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
                "price": j[4],
                "adult": j[5],
                "children": j[6],
                "invalid": j[7],
            })
        res.append(pr)
    context = {
        "lst": res
    }

    if request.method == "POST":
        rq = dict(request.POST)
        print("timetable", request.POST)
        if len(list(rq.keys())) > 1:
            ids = list(rq.keys())[-1]
            Programm.objects.filter(id=ids).delete()
        return redirect('../admin/')

    return render(request, "main_admins.html", context)

def plot_page(request):
    import matplotlib.pyplot as plt

    # Предположим, что у вас есть данные экскурсий в формате (день_недели, начало_час, конец_час)

    excursions = []

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
    for i in days[now_weekday - 1:len(days)]:
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
    colors = ["red", "orange", "yellow", "blue", "green", "lightblue", "black", "purple"]
    for i in programms:
        if i.day_start - now_day <= 6:
            lst[list(lst.keys())[i.day_start - now_day]].append(
                [int(i.hour_start), int(i.hour_start) + int(i.length), random.choice(colors), i.id])
    print("LST: ", lst)
    for i in lst:
        if len(lst[i]) > 0:
            for j in lst[i]:
                excursions.append((str(i), j[0], j[1], j[3], j[2]))
    print(excursions)
    fig, ax = plt.subplots()
    days = list(lst.keys())
    # Устанавливаем интервалы для дней недели и времени
    times = [[[] for i in range(0, 24)] for i in range(len(days))]
    for i in excursions:
        print(i)
        for j in range(i[1], i[2]):
            print(j, days.index(i[0]))
            times[days.index(i[0])][j].append([i[3], i[4]])
    for i in times:
        print(*i)

    # Создаем график
    def exc_name_ind(name):
        for i in range(len(excursions)):
            if excursions[i][3] == name:
                return i

    # Отображаем данные экскурсий на диаграмме Ганта
    for i in range(len(times)):
        for j in range(len(times[i])):
            idx = len(times[i][j])
            if idx != 0:
                idx = 1 / idx
                if idx == 1:
                    indexes = [0]
                else:
                    indexes = [0 for i in range(len(times[i][j]))]

                    print(indexes, end=" ")
                    key = 1
                    for q in range(len(times[i][j]) // 2 - 1, -1, -1):
                        indexes[q] -= key * (0.15)
                        key += 1
                    key = 1
                    for q in range(len(times[i][j]) // 2, len(times[i][j])):
                        indexes[q] += key * (0.15)
                        key += 1
                print(indexes, len(times[i][j]))
                for r in range(len(times[i][j])):
                    index_exc = exc_name_ind(times[i][j][r][0])
                    if len(times[i][j][r]) > 0 and excursions[index_exc][1] == j:
                        ax.barh(i + indexes[r], excursions[index_exc][2] - excursions[index_exc][1], left=j,
                                height=0.15, align='center', color=times[i][j][r][1])

    # Добавляем клеточную сетку
    ax.grid(True)

    # Настройка осей и меток
    ax.set_yticks(range(len(days)))
    ax.set_yticklabels(days)  # Изменяем порядок дней недели на обратный
    ax.set_xticks(list(range(0, 24)))
    ax.set_xlabel('Время')
    ax.set_ylabel('День недели')
    ax.set_title('Диаграмма Ганта для экскурсий')
    plt.savefig('static/dg.png', format='png')
    plt.savefig('static/dg.png', format='png')
    return render(request, "plot.html")

@login_required
def museum_info_page(request):
    places = Place.objects.filter()
    context = {
        "places": places,
    }
    return render(request, "museum_info.html", context)

def timetable_client_page(request):
    user = User.objects.get(username=request.user)

    rgs = list(Registr.objects.filter(user=user))
    print(rgs)
    programms = []
    for i in rgs:
        programms.append(list(Programm.objects.filter(id=int(i.programm_id.id)))[0])
    print(programms)
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
    for i in days[now_weekday - 1:len(days)]:
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
                [i.name, str(i.hour_start).zfill(2), str(i.minute_start).zfill(2), i.length, i.price_adult, i.id])

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
                "price": j[4],
                "id": j[5]
            })
        res.append(pr)
    context = {
        "lst": res
    }
    if request.method == "POST":
        rq = dict(request.POST)
        ids = list(rq.keys())[-1]
        Registr.objects.filter(programm_id=ids).delete()
        print("timetable", request.POST)
        return redirect('../timetable_client/')

    return render(request, "timetable_client.html", context)

def one_reserv_page(request):
    key = 0
    programs = []
    ids = ""
    if request.method == 'POST' and "adults" not in request.POST:
        key += 1
        print("1:::::  ", request.POST)
        selected_checkboxes = request.POST.getlist('checkbox_name')
        print(selected_checkboxes)

        if len(selected_checkboxes) == 0:
            return redirect("/basket_reserv")
        for checkbox in selected_checkboxes:
            ids += f"{checkbox} "
            pgs = Programm.objects.filter(id=checkbox)
            for i in list(pgs):
                if i not in programs:
                    programs.append(i)
        print("1")
    context= dict()
    names = ""
    timetable = []
    for i in programs:
        names += f"{i.name}, "
    names = names[:len(names)-2] + ":"
    for i in programs:
        timetable.append(f"{i.hour_start}:{i.minute_start} {i.day_start}.{i.month_start}\n")
    context["timetable"] = timetable
    context["names"] = names
    context["ids"] = ids
    red_flag = "ВСЕ ПРОВЕРЕНО"
    for i in range(len(programs)):
        for j in range(i+1, len(programs)):
            if (programs[i].day_start == programs[j].day_start and programs[i].month_start == programs[j].month_start):
                if (programs[i].hour_start > programs[j].hour_start):
                    if ( programs[i].hour_start <= programs[j].hour_start + programs[j].length):
                        red_flag = "ПРОБЛЕМА СО ВРЕМЕНЕМ"
                elif (programs[j].hour_start > programs[i].hour_start):
                    if ( programs[j].hour_start <= programs[i].hour_start + programs[i].length):
                        red_flag = "ПРОБЛЕМА СО ВРЕМЕНЕМ"
                elif (programs[j].hour_start == programs[i].hour_start):
                    if (programs[i].minute_start > programs[j].minute_start):
                        if ( programs[i].minute_start <= programs[j].minute_start + programs[j].length * 60):
                            red_flag = "ПРОБЛЕМА СО ВРЕМЕНЕМ"
                    elif (programs[j].minute_start > programs[i].minute_start):
                        if ( programs[j].minute_start <= programs[i].minute_start + programs[i].minute_start * 60):
                            red_flag = "ПРОБЛЕМА СО ВРЕМЕНЕМ"
    user = User.objects.get(username=request.user)
    rgs = Registr.objects.filter(user=user)
    for i in list(rgs):
        if i in programs:
            if red_flag == "ВСЕ ПРОВЕРЕНО":
                red_flag = "УЖЕ СУЩЕСТВУЮТ ЗАПИСИ НА ЭТИ ПРОГРАММЫ"
            else:
                red_flag += " + УЖЕ СУЩЕСТВУЮТ ЗАПИСИ НА ЭТИ ПРОГРАММЫ"

    context["red_flag"] = red_flag
    if request.method == "POST":
        print(request.POST)
        if "adults" in request.POST:
            req = dict(request.POST)
            ids = list(map(int, list(req.keys())[-1].split()))
            programs = []
            for i in ids:
                programs.append(list(Programm.objects.filter(id=i))[0])
            print("2", programs, list(req.keys())[-1])
            redircts = []
            for i in programs:
                adult = int(request.POST.get("adults"))
                children = int(request.POST.get("children"))
                invalid = int(request.POST.get("invalid"))
                capacity = int(i.capacity)
                rgs = Registr.objects.filter(programm_id=i)
                adult_count = 0
                children_count = 0
                invalid_count = 0
                for j in list(rgs):
                    adult_count += int(j.adult_count)
                    children_count += int(j.children_count)
                    invalid_count += int(j.invalid_count)
                if adult_count + children_count + invalid_count + adult + children + invalid > capacity:
                    redircts.append(i)
                else:
                    record = Registr(
                        programm_id=i,
                        user=user,
                        adult_count = request.POST.get("adults"),
                        children_count = request.POST.get("children"),
                        invalid_count = request.POST.get("invalid"),
                        status="None"
                    )
                    record.save()
            if len(redircts) > 0:
                ids = ""
                for i in redircts: ids += f"{i.id} "
                return redirect(f"../error_count/{ids}")
            return redirect('../timetable_client/')
    return render(request, "one_reserv.html", context)

def registr_page(request, id):
    programm = list(Programm.objects.filter(id=id))[0]
    context = dict()
    context["programm"] = programm
    rgss = list(Registr.objects.filter(programm_id=programm))
    rgs = list()
    for i in rgss:
        inf = list(UserInfo.objects.filter(user=i.user))[0]
        dct = {
            "pr": i,
            "us": inf
        }
        rgs.append(dct)
    context["rgs"] = rgs
    if request.method == "POST":
        print(request.POST)
        req = dict(request.POST)
        ids = int(list(req.keys())[-1])
        rg = list(Registr.objects.filter(id=ids))[0]
        rg.status = "Done"
        rg.save()

    return render(request, "registr.html", context)


def error_count_page(request, ids):
    programms = []
    ids = list(map(int, ids.split()))
    print(ids)
    for j in ids:
        programms.append(list(Programm.objects.filter(id=j))[0].name)
    print(programms)
    if request.method == "POST":
        print(request.POST)
        return redirect("/basket/")
    return render(request, "error_count.html", context={"programms": programms})


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
    for i in days[now_weekday - 1:len(days)]:
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
        if i.day_start - now_day <= 6:
            lst[list(lst.keys())[i.day_start - now_day]].append([i.name, str(i.hour_start).zfill(2), str(i.minute_start).zfill(2), i.length, i.price_adult, i.id])

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
                "price": j[4],
                "id": j[5]
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
    print(days[now_weekday - 1:len(days):])
    for i in days[now_weekday - 1:len(days):]:
        print(i)
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
    print(programms)
    for i in programms:
        change_time(i)
        if i.day_start - now_day <= 6:
            lst[list(lst.keys())[i.day_start - now_day]].append(
                [i.name, str(i.hour_start).zfill(2), str(i.minute_start).zfill(2), i.length, i.price_adult, i.id])

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
                "price": j[4],
                "id": j[5]
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
    return render(request, "all_museums.html", context)

def admin_reserv_page(request):
    programms = list(Programm.objects.filter())
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
    for i in days[now_weekday - 1:len(days)]:
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
        if i.day_start - now_day <= 6:
            lst[list(lst.keys())[i.day_start - now_day]].append([i.name, str(i.hour_start).zfill(2), str(i.minute_start).zfill(2), i.length, i.price_adult, i.id])

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
                "price": j[4],
                "id": j[5]
            })
        res.append(pr)
    context = {
        "lst": res
    }

    return render(request, "admin_reserv.html", context)

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
