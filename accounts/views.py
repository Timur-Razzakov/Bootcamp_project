import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from icecream import ic
from django.views.decorators.csrf import csrf_exempt
from accounts.forms import UserLoginForm, UserRegistrationForm, UserRequisitesForm, Subscription, \
    UserUpdateForm
from msg_sender.models import Channel, Notification_group
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
    emp_email =[]
    emp_channel=[]
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
        # for item in user_details:
        """ Функция для заполнения формы подписки   """
        subsc = Subscription.objects.create()
        user_data = User.objects.filter(email=request.user).values('id', 'email', 'notification_group')
        ic(user_data)
        for item in user_data:
            subsc.notification_group.add(item['notification_group'])
            empl_requisites = Empl_requisites.objects.filter(employee=item['id'])
            for item in empl_requisites:
                subsc.employee_requisites.add(item)
        subsc.save()
        form = UserRegistrationForm(
            initial={'email': user.email,
                     'notification_group': user.notification_group})  # выводит уже введённые данные
        return render(request, 'msg_sender/home.html',
                      {'form': form})
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


"""Функция для сбора всех данных и отправка в сервисы для рассылки нотификаций
"""


# TODO:пересмотреть сохранение, сохраняет только одного пользователя #Done!!
# TODO: Спросить у Ивана могут ли к нам попасть реквизиты залётных пользователей?
# TODO: разделить отправку сообщений, либо добавиnm
@csrf_exempt
def save_to_result(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        qs = Subscription.objects.filter(notification_group=data['notification_group']).values(
            'employee_requisites', 'notification_group')
        res_for_send = Result.objects.create()
        for item in qs:
            employee_requisite = Empl_requisites.objects.filter(id=item['employee_requisites']).values(
                'channel', 'user_details')
            for item in employee_requisite:
                channel_names = Channel.objects.get(id=item['channel'])
                employee_detail = Empl_requisites.objects.filter(user_details=item['user_details'])
                for item in employee_detail:
                    res_for_send.employee_details.add(item)
                # ntf_templates = NTF_type_for_channel.objects.filter(id=item['channel']).values('templates_for_massage')
                # for template in ntf_templates:
                #     ic(template['templates_for_massage'])
                #     res_for_send.message = template['templates_for_massage'].format(message=data['message'],
                #                                                                                     created_at=data['created_at'],
                #                                                                                     url=data['url']))
                res_for_send.channels.add(channel_names)
                res_for_send.status = data['status']
                res_for_send.url = data['url']
                res_for_send.created_at = data['created_at']
                res_for_send.message_title = data['title']
                res_for_send.message = data['message']
            res_for_send.save()

        messages.success(request, 'Данные сохранены')
        return redirect('/')
