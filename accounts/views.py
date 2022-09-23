import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from icecream import ic
from django.views.decorators.csrf import csrf_exempt
from accounts.forms import UserLoginForm, UserRegistrationForm, UserRequisitesForm, Subscription, \
    UserUpdateForm
from msg_sender.models import Channel, Notification_group, NTF_type_for_channel, Notification
from django.contrib.auth.decorators import login_required

User = get_user_model()
from .models import Empl_requisites, Subscription, Result

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
    ic(user)
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
        ic(User.objects.get(email=request.user))
        for item in user_data:
            subsc.employee = User.objects.get(pk=item['id'])
            subsc.notification_group.add(item['notification_group'])
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
                print(data)
                user.email = data['email']
                user.notification_group.set(data['notification_group'])
                user.save()
                messages.success(request, 'Данные сохранены.')
                return redirect('update')
        form = UserRegistrationForm(
            initial={'email': user.email})  # выводит уже введённые данные
        return render(request, 'accounts/update.html',
                      {'form': form, })
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


"""

Функция для сбора всех данных и отправка в сервисы для рассылки нотификаций

"""


# TODO: Сохранить нотификации в result
@csrf_exempt
def save_to_result(request):
    global ntf_templates
    if request.method == "POST":
        data = json.loads(request.body.decode())
        channel_names = Channel.objects.all()
        for channel_name in channel_names:  # tg
            res_for_send = Result.objects.create()
            res_for_send.channels = channel_name
            all_requisites = Empl_requisites.objects.filter(channel=channel_name)
            # TODO: Нужно разделить данные, те, что есть и тех которые получил от внеш сервисов и отпр им сообщение тоже
            # получаем реквизиты пользователя, переданные от внешних сервисов
            # empl_recipients = data['recipient']
            for requisite in all_requisites:
                res_for_send.employee_details.add(requisite)
                # if str(requisite) in empl_recipients:
                #     empl_recipients.remove(requisite)
                #     ic(empl_recipients)

            ntf_templates = NTF_type_for_channel.objects.get(channel=channel_name)
            content = ntf_templates.templates_for_massage.format(message_title=data['title'],
                                                                 status=data['status'],
                                                                 message=data['message'],
                                                                 created_at=data['created_at'],
                                                                 url=data['url'])
            res_for_send.message = content
            res_for_send.created_at = data['created_at']
            res_for_send.save()

        messages.success(request, 'Данные сохранены')
        return redirect('/')
