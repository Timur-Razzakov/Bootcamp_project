import datetime as dt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from accounts.forms import UserLoginForm, UserRegistrationForm

User = get_user_model()

"""Функция для авторизации"""


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


"""Функция выхода"""


def logout_view(request):
    logout(request)
    return redirect('home')



""" Функция для создание нового пользователя """


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)  # instans) commit=False-->исп для полного соединения с базой
        data = form.cleaned_data
        new_user.tg_nickname = data['tg_nickname']
        new_user.tg_channel = data['tg_channel']
        new_user.set_password(form.cleaned_data['password'])  # ЗАШИФРОВЫВАЕТ пароль
        new_user.send_email = data['receiver']
        if new_user.send_email == True:
            new_user.send_to_email = data['send_to_email']
            new_user.send_to_tg_channel = data['send_to_tg_channel']
            new_user.send_to_tg_privet_channel = data['send_to_tg_privet_channel']
        else:
            new_user.save()
        new_user.save()
        messages.success(request, 'Пользователь добавлен в систему.')
        return render(request, 'accounts/login.html',
                    {'new_user': new_user})
    return render(request, 'accounts/registration.html', {'form': form})

#
# """
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
