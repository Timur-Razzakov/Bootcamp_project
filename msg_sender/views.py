import datetime
import json
import pika
from django.contrib import messages
from django.contrib.auth import get_user_model
import requests
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from icecream import ic
from psycopg2.extensions import JSON

from accounts.models import Subscription, Empl_requisites
from natification_service.settings import (
    EMAIL_HOST_USER
)
from .forms import NTF_typeForm
from .models import Service, Channel, Notification_group, Notification, Result, NTF_type_for_channel


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


@csrf_exempt
def receive(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        ntf_group = Notification_group.objects.get(id=data["notification_group"])
        ntf = Notification.objects.create()
        ntf.title = data["title"]
        ntf.status = data["status"]
        ntf.url = data["url"]
        ntf.message = data["message"]
        ntf.created_at = data["created_at"]
        ntf.ntf_group = ntf_group
        ntf.save()
        ic('Данные сохранены.')
        messages.success(request, 'Данные сохранены.')
        return redirect('/')


"""Функция для заполнения шаблонов пользователями """


def ntf_templates_view(request):
    form = NTF_typeForm(request.POST or None)
    if form.is_valid():
        new_ntf_templates = form.save()
        data = form.cleaned_data
        for item in data['ntf_group']:
            new_ntf_templates.ntf_group.add(Notification_group.objects.get(group_name=item))
        for item in data['channel']:
            new_ntf_templates.channel.add(Channel.objects.get(name=item))
        new_ntf_templates.templates_for_massage = data['templates_for_massage']
        new_ntf_templates.save()
        messages.success(request, 'Данные сохранены')
        return render(request, 'msg_sender/my_templates.html',
                      {'new_ntf_templates': new_ntf_templates})  # 'accounts/login.html'
    return render(request, 'msg_sender/add_ntf_templates.html', {'form': form})


"""Функция для сбора всех данных и отправка в сервисы для рассылки нотификаций"""
"""
class Result(models.Model):
    massage = models.TextField(verbose_name="текст сообщения")=
    sending_status = models.CharField(verbose_name='sending_status', max_length=30, blank=True)
    process_date = models.DateField(verbose_name='send_to', blank=True)

"""


@csrf_exempt
def save_to_result(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        ic(data)
        qs = Subscription.objects.filter(notification_group=data['notification_group']).values(
            'employee_requisites', 'notification_group')
        ic(qs)
        res_for_send = Result.objects.create()
        for item in qs:
            employee_requisite = Empl_requisites.objects.filter(id=item['employee_requisites']).values(
                'channel', 'user_details')
            for item in employee_requisite:
                channel_names = Channel.objects.get(id=item['channel'])
                ntf_templates = NTF_type_for_channel.objects.filter(id=item['channel']).values('templates_for_massage')
                for template in ntf_templates:
                    ic(template['templates_for_massage'])
                    res_for_send.message = template['templates_for_massage']
                res_for_send.channels = Channel.objects.get(id=item['channel'])
                employee_details = json.dumps({f'{channel_names}': item['user_details']})
                res_for_send.employee_details = employee_details
            res_for_send.status = data['status']
            res_for_send.url = data['url']
            res_for_send.created_at = data['created_at']
            res_for_send.message_title = data['title']
            res_for_send.save()
            messages.success(request, 'Данные сохранены')
        return redirect('/')
