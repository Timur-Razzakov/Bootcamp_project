import datetime as dt

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from icecream import ic

from accounts.forms import UserLoginForm, UserRegistrationForm, UserRequisitesForm, Subscription, \
    UserUpdateForm
from msg_sender.models import Channel, Service, Notification_group
from django.contrib.auth.decorators import login_required

User = get_user_model()
from .models import Empl_requisites, Subscription

"""Функция для авторизации"""

def login_view(request):
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        employee_requisites = Empl_requisites.objects.filter(employee=request.user)
        if employee_requisites.exists():
            return redirect('home')
        else:
            return redirect('user_requisites')
    return render(request, 'accounts/login.html', {'form': form})


"""Функция выхода"""


def logout_view(request):
    logout(request)
    return redirect('home')


""" Функция для создание нового пользователя  """
"""https://ru.stackoverflow.com/questions/739037/"""


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save()  # instans) commit=False-->исп для полного соединения с базой
        data = form.cleaned_data
        for item in data['channel']:
            new_user.channel.add(Channel.objects.get(name=item))
        for item in data['notification_group']:
            new_user.notification_group.add(Notification_group.objects.get(group_name=item))
        new_user.set_password(form.cleaned_data['password'])  # ЗАШИФРОВЫВАЕТ пароль
        new_user.send_email = data['receiver']
        # new_user.channel = data['channel']
        # new_user.notification_group = data['notification_group']
        new_user.save()
        return render(request, 'accounts/registered.html', {'new_user': new_user})  # 'accounts/login.html'
    return render(request, 'accounts/registration.html', {'form': form})


""" Функция для получения реквизитов пользователя """


@login_required
def requisites_view(request):
    form = UserRequisitesForm(request.POST or None)
    if form.is_valid():
        email = User.objects.get(email=request.user)
        user_requisites = form.save(commit=False)
        data = form.cleaned_data
        user_requisites.employee = email
        user_requisites.tg_nickname = data['tg_nickname']
        user_requisites.tg_channel = data['tg_channel']
        user_requisites.phone_number = data['phone_number']
        user_requisites.save()
        """ Функция для заполнения формы подписки   """
        subsc = Subscription.objects.create()
        user_data = User.objects.filter(email=request.user).values('id', 'email', 'notification_group',
                                                                   'channel')
        for item in user_data:
            subsc.employee = (User.objects.get(email=item['email']))
            subsc.employee_requisites.add(Empl_requisites.objects.get(employee=item['id']))
            subsc.channel.add(Channel.objects.get(id=item['channel']))
            subsc.notification_group.add(Notification_group.objects.get(id=item['notification_group']))
        subsc.save()

        return render(request, 'msg_sender/home.html',
                      {'user_requisites': user_requisites})
    return render(request, 'accounts/get_user_requisites.html', {'form': form})


""" Функция для заполнения формы подписки   """

# @login_required
# def subscription_View(request):
#     subsc = Subscription.objects.create()
#     user_data = User.objects.filter(email=request.user).values('id', 'email', 'notification_group', 'channel')
#     for item in user_data:
#         subsc.employee = (User.objects.get(email=item['email']))
#         subsc.employee_requisites.add(Empl_requisites.objects.get(employee=item['id']))
#         subsc.channel.add(Channel.objects.get(id=item['channel']))
#         subsc.notification_group.add(Notification_group.objects.get(id=item['notification_group']))
#     subsc.save()


FORMS = [
    ("registration", UserRegistrationForm),
    ("requisites", UserRequisitesForm)
]

TEMPLATES = {
    "registration": "registration.html",
    "requisites": "get_user_model.html"
}
"""
Функция для обновлений данных указанных ранее 
"""

def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print(data)
                user.email = data['email']
                user.channel.set(data['channel'])
                user.notification_group.set(data['notification_group'])

                user.save()
                messages.success(request, 'Данные сохранены.')
                return redirect('update')
        form = UserRegistrationForm(
            initial={'email': user.email})  # выводит уже введённые данные
        return render(request, 'accounts/update.html',
                      {'form': form,})
    else:
        return redirect('login')


"""Функция для обновления реквизитов пользователя"""


def requisite_update_view(request):
    if request.method == 'POST':
        requisites_form = UserRequisitesForm(request.POST or None)
        if requisites_form.is_valid():
            data = requisites_form.cleaned_data
            print(data)

            # qs = Error.objects.filter(created_at=dt.date.today())
            # if qs.exists():
            #     err = qs.first()
            #     data = err.data.get('user_data', [])
            #     data.append({'city': city, 'email': email, 'speciality': speciality})
            #     err.data['user_data'] = data
            #     err.save()
            # else:
            #     data = [{'city': city, 'email': email, 'speciality': speciality}]
            #     Error(data=f"user_data:{data}").save()
            # messages.success(request, 'Данные отправлены администрации.')
            # return redirect('update')
        else:
            return redirect('update')
    else:
        return redirect('home')


"""Функция для удаления пользователя"""


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удалён :(')
    return redirect('home')
