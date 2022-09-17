import datetime
import json
import pika
from django.contrib import messages
from django.contrib.auth import get_user_model
import requests
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from icecream import ic

from accounts.models import Subscription, Empl_requisites
from natification_service.settings import (
    EMAIL_HOST_USER
)
from .forms import NTF_typeForm
from .models import Service, Channel, Notification_group, Notification, NTF_type_for_channel


def home_view(request):
    services = Service.objects.all()
    return render(request, 'msg_sender/home.html', {'services': services})


""" Получаем данные из внешнего сервиса и сохраняем в бд"""
# # Возвращает пользователя по умолчанию
User = get_user_model()
ADMIN_USER = EMAIL_HOST_USER


# TODO: добавить json для отправки имаил от внешних сервисов и распаковка на нашем
# TODO: разобраться с шаблонами и вставка в них сообщений

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
        ntf.recipient = data["email"]
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

