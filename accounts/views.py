from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from icecream import ic

from accounts.forms import UserLoginForm, UserRegistrationForm, UserRequisitesForm, UserUpdateForm, \
    UserRequisitesUpdateForm
from msg_sender.models import Channel, Notification_group

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
        for item in data['notification_group']:
            new_user.notification_group.add(Notification_group.objects.get(group_name=item))
        new_user.set_password(form.cleaned_data['password'])  # ЗАШИФРОВЫВАЕТ пароль
        new_user.send_email = data['receiver']
        new_user.save()
        return render(request, 'accounts/registered.html', {'new_user': new_user})  # 'accounts/login.html'
    return render(request, 'accounts/registration.html', {'form': form})


""" Функция для получения реквизитов пользователя """


@login_required
def requisites_view(request):
    form = UserRequisitesForm(request.POST or None)
    user = request.user
    emp_email = []
    emp_channel = []
    if form.is_valid():
        data = form.cleaned_data
        user_requisites = form.save(commit=False)
        user_details = data['user_details'].split(',')
        email = User.objects.get(email=data['employee'])
        emp_email.append(email)
        channel = Channel.objects.get(name=data['channel'])
        emp_channel.append(channel)
        user_requisites.user_details = user_details[0]
        user_requisites.save()
        for item in user_details[1::]:
            requis = Empl_requisites.objects.create()
            requis.employee = email
            requis.channel = channel
            requis.user_details = item
            requis.save()
        """ Функция для заполнения формы подписки   """
        subsc = Subscription.objects.create()
        user_data = User.objects.filter(email=request.user).values('id', 'notification_group')
        ic(user_data)
        for item in user_data:
            subsc.employee = User.objects.get(pk=item['id'])
            subsc.notification_group.add(Notification_group.objects.get(pk=item['notification_group']))
            empl_requisites = Empl_requisites.objects.filter(employee=item['id']).values('id', 'channel',
                                                                                         )
            for item in empl_requisites:
                # subsc.employee_requisites.add(item['id'])
                subsc.channels.add(Channel.objects.get(pk=item['channel']))
        subsc.save()
        form = UserRegistrationForm(
            initial={'email': user.email,
                     'notification_group': user.notification_group})  # выводит уже введённые данные
        return render(request, 'msg_sender/home.html',
                      {'form': form})
    return render(request, 'accounts/get_user_requisites.html', {'form': form})


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
                user.email = data['email']
                user.notification_group.set(data['notification_group'])
                subscription = Subscription.objects.get(employee=user)
                subscription.notification_group.set(data['notification_group'])
                subscription.save()
                # for item in data['notification_group']:
                #     user.notification_group.add(Notification_group.objects.get(group_name=item))
                c_user = authenticate(email=data['email'], password=data['current_password'])
                if c_user is not None:
                    messages.error(request, 'Неверный пароль или Логин.')
                else:
                    user.receiver = data['receiver']
                    user.set_password(form.cleaned_data['password'])  # ЗАШИФРОВЫВАЕТ пароль
                    user.save()
                messages.success(request, 'Данные сохранены.')
                return redirect('update')
            else:
                print("Form not valid")
        # form = UserUpdateForm(
        #     initial={'email': user.email,
        #              'receiver': user.receiver})  # выводит уже введённые данные
        all_notification_groups = Notification_group.objects.all()
        context = {'email': user.email,
                   'receiver': user.receiver,
                   'user_notification_groups': user.notification_group.all(),
                   'all_notification_groups': all_notification_groups}

        return render(request, 'accounts/update.html', context)
    else:
        return redirect('login')


"""Функция для обновления реквизитов пользователя"""


def requisite_list_view(request):
    user = request.user
    requisites = Empl_requisites.objects.filter(employee=user)
    return render(request, "accounts/requisite_list.html", {'requisites': requisites})


def requisite_update_view(request, pk):
    if request.method == 'POST':
        requisite_update_form = UserRequisitesUpdateForm(request.POST)
        ic(requisite_update_form)
        if requisite_update_form.is_valid():
            data = requisite_update_form.cleaned_data
            requisite = Empl_requisites.objects.get(id=pk)
            requisite.channel = Channel.objects.get(name=data['channel'])
            requisite.user_details = data['user_details']
            requisite.save()
            return redirect('requisites_update', pk)
        else:
            messages.error(request, 'Данные не верны!!')
            return redirect('requisites_update', pk)
    else:
        requisite = Empl_requisites.objects.get(id=pk)
        channels = Channel.objects.all()
        context = {'requisite': requisite, 'channels': channels}
        return render(request, 'accounts/requisite_update.html', context)


"""Функция для удаления пользователя"""


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удалён :(')
    return redirect('home')
