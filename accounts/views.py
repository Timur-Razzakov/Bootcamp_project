import datetime as dt

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from icecream import ic

from accounts.forms import UserLoginForm, UserRegistrationForm, UserRequisitesForm
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
        return render(request, 'accounts/registered.html',{'new_user': new_user})  # 'accounts/login.html'
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


# Функция для обновлений данных указанных ранее
# """
#
#
# def update_view(request):
#     if request.user.is_authenticated:
#         user = request.user
#         if request.method == 'POST':
#             form = UserUpdateForm(request.POST)
#             if form.is_valid():
#                 data = form.cleaned_data
#                 user.tg_nickname = data['tg_nickname']
#                 user.tg_channel = data['tg_channel']
#                 user.send_to_email = data['send_to_email']
#                 user.send_to_tg_channel = data['send_to_tg_channel']
#                 user.send_to_private_channel = data['send_to_private_channel']
#                 user.save()
#                 messages.success(request, 'Данные сохранены.')
#                 return redirect('update')
#         form = UserUpdateForm(
#             initial={'tg_nickname': user.tg_nickname, 'tg_channel': user.tg_channel,
#                      'send_to_email': user.send_to_email, 'send_to_tg_channel': user.send_to_tg_channel,
#                      'send_to_private_channel': user.send_to_private_channel})
#         return render(request, 'accounts/update.html',
#                       {'form': form, 'contact_form': contact_form})
#     else:
#         return redirect('login')


"""Функция для удаления пользователя"""


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удалён :(')
    return redirect('home')
