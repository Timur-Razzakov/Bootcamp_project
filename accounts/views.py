import datetime as dt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from accounts.forms import UserLoginForm, UserRegistrationForm, UserRequisitesForm

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

"""и"""

""" Функция для получения реквизитов пользователя """
def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    requisites_form = UserRequisitesForm(request.POST or None)
    if form.is_valid():
        user_requisites = requisites_form.save(commit=False)
        new_user = form.save(commit=False)  # instans) commit=False-->исп для полного соединения с базой
        data_2 = requisites_form.cleaned_data
        data = form.cleaned_data
        new_user.set_password(form.cleaned_data['password'])  # ЗАШИФРОВЫВАЕТ пароль
        user_requisites.tg_nickname = data_2['tg_nickname']
        user_requisites.tg_channel = data_2['tg_channel']
        user_requisites.phone_number = data_2['phone_number']
        new_user.send_email = data['receiver']
        if new_user.send_email == True:
            new_user.send_to_email = data['send_to_email']
            new_user.send_to_tg_channel = data['send_to_tg_channel']
            new_user.send_to_tg_privet_channel = data['send_to_tg_privet_channel']
        else:
            new_user.save()
        new_user.save()
        user_requisites.save()
        messages.success(request, 'Пользователь добавлен в систему.')
        return render(request, 'accounts/login.html',
                      {'new_user': new_user, 'user_requisites': user_requisites})
    return render(request, 'accounts/registration.html', {'form': form, 'requisites_form': requisites_form})


""" Функция для получения реквизитов пользователя """


# def requisites_view(request):
#     form = UserRequisitesForm(request.POST or None)
#     if form.is_valid():
#         user_requisites = form.save(commit=False)
#         data = form.cleaned_data
#
#         user_requisites.channel = data['tg_nickname']
#         user_requisites.tg_nickname = data['tg_nickname']
#         user_requisites.tg_channel = data['tg_channel']
#         user_requisites.phone_number = data['phone_number']
#         user_requisites.save()


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
