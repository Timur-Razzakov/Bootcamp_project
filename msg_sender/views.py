import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import NotificationForm
# Create your views here.
from .models import Service, Notification, Notification_group
from accounts.models import MyUser


def home_view(request):
    services = Service.objects.all()
    return render(request, 'msg_sender/home.html', {'services': services})


# def show_service(request):
#     services = Service.objects.all()
#     return render(request, 'msg_sender/home.html', {'services': services})


""" Получаем данные из внешнего сервиса и сохраняем в бд"""


@csrf_exempt
def receive(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        print(data)
        # Notification.objects.create(**data)
        ntf_group = Notification_group.objects.get(description=data["notification_group"])
        print(ntf_group)
        ntf = Notification.objects.create()
        print(ntf)
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
