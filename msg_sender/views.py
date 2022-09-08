import datetime
import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from icecream import ic

from accounts.models import Subscription, Empl_requisites
from natification_service.settings import (
    EMAIL_HOST_USER
)
from .models import Service, Channel



def home_view(request):
    services = Service.objects.all()
    return render(request, 'msg_sender/home.html', {'services': services})


# def show_service(request):
#     services = Service.objects.all()
#     return render(request, 'msg_sender/home.html', {'services': services})


""" Получаем данные из внешнего сервиса и сохраняем в бд"""
# # Возвращает пользователя по умолчанию
User = get_user_model()
ADMIN_USER = EMAIL_HOST_USER


# @csrf_exempt
# def receive(request):
#     if request.method == "POST":
#         data = json.loads(request.body.decode())
#         ntf_group = Notification_group.objects.get(id=data["notification_group"])
#         ntf = Notification.objects.create()
#         ntf.title = data["title"]
#         ntf.status = data["status"]
#         ntf.url = data["url"]
#         ntf.message = data["message"]
#         ntf.created_at = data["created_at"]
#         ntf.ntf_group = ntf_group
#
#         ntf.save()
#         messages.success(request, 'Данные сохранены.')
#         return redirect('/')

"""Функция для сбора всех данных и отправка в сервисы для рассылки нотификаций"""
@csrf_exempt
def receive(request):
    results = []
    if request.method == "POST":
        data = json.loads(request.body.decode())
        qs = Subscription.objects.filter(notification_group=data['notification_group']).values(
            'employee', 'channel', 'employee_requisites', 'notification_group')
        for item in qs:
            channel_names = Channel.objects.get(id=item['channel'])
            if channel_names == Channel.objects.get(name='email'):
                employee = User.objects.filter(notification_group=item['notification_group']).values(
                    'email')
                for email in employee:
                    employee_email = {
                        'channel': channel_names,
                        'title': data['title'],
                        'status': data['status'],
                        'created_at': data['created_at'],
                        'message': data['message'],
                        'url': data['url'],
                        'email': email['email']
                    }
                results.append(employee_email)
            else:
                ic(item['employee'])
                employee_requisites = Empl_requisites.objects.filter(employee=item['employee']).values(
                    'tg_nickname', 'tg_channel', 'phone_number')
                for employee_requisite in employee_requisites:
                    employee_requisites = {
                        'channel': channel_names,
                        'title': data['title'],
                        'status': data['status'],
                        'created_at': data['created_at'],
                        'message': data['message'],
                        'url': data['url'],
                        'tg_nickname': employee_requisite['tg_nickname'],
                        'tg_channel': employee_requisite['tg_channel'],
                        'phone_number': employee_requisite['phone_number']
                    }
                results.append(employee_requisites)

        ic(results)

        messages.success(request, 'Данные сохранены.')
        return redirect('/')
