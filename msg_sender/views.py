import json
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import NotificationForm
# Create your views here.
from .models import Service, Notification, Notification_group
from accounts.models import MyUser
from natification_service.settings import (
    EMAIL_HOST_USER
)
import time
from django.core.mail import EmailMultiAlternatives
import datetime

today = datetime.date.today()
subject = f"Нотификация {today}"
text_content = f"Пробная нотификация {today}"


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
        ntf_group = Notification_group.objects.get(description=data["notification_group"])
        ntf = Notification.objects.create()
        ntf.title = data["title"]
        ntf.status = data["status"]
        ntf.url = data["url"]
        ntf.message = data["message"]
        ntf.created_at = data["created_at"]
        ntf.email = data["email"]
        ntf.ntf_group = ntf_group

        ntf.save()
        messages.success(request, 'Данные сохранены.')
        return redirect('/')

#
# @csrf_exempt
# def receive(request):
#     if request.method == "POST":
#         data = json.loads(request.body.decode())
#         qs = User.objects.filter(receiver=True ).values('email', 'channel', 'service')
#         print(len(qs))
#         user_dict = {}
#         for item in qs:
#             print(item)
#         # ntf_group = Notification_group.objects.get(description=data["notification_group"])
#         # ntf = Notification.objects.create()
#         # ntf.title = data["title"]
#         # ntf.status = data["status"]
#         # ntf.url = data["url"]
#         # ntf.message = data["message"]
#         # ntf.created_at = data["created_at"]
#         # ntf.email = data["email"]
#         # ntf.ntf_group = ntf_group
#
#         # ntf.save()
#         messages.success(request, 'Данные сохранены.')
#         return redirect('/')
