import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Subscription
from natification_service.settings import (
    EMAIL_HOST_USER
)
from .forms import NTF_typeForm
from .models import Service, Notification_group, Notification, NTF_type_for_channel


def home_view(request):
    services = Service.objects.all()
    notification_groups = Notification_group.objects.all()
    try:
        user = User.objects.get(email=request.user)
        subscripton = Subscription.objects.get(employee=user)
        context = {'services': services, 'notification_groups': notification_groups,
                   'subscripton': subscripton}
    except:
        context = {'services': services, 'notification_groups': notification_groups}

    return render(request, 'msg_sender/home.html', context)


# # Возвращает пользователя по умолчанию
User = get_user_model()
ADMIN_USER = EMAIL_HOST_USER

"""Функция для заполнения шаблонов пользователями """


def ntf_templates_view(request):
    templates = NTF_type_for_channel.objects.all()
    return render(request, "msg_sender/my_templates.html", {'templates': templates})


def template_update_view(request, pk):
    template = NTF_type_for_channel.objects.get(pk=pk)
    if request.method == "POST":
        form = NTF_typeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            template.ntf_group = data['ntf_group']
            template.channel = data['channel']
            template.templates_for_massage = data['templates_for_massage']
            template.save()
            messages.success(request, 'Данные изменены!!')
            return redirect('my_templates')
    form = NTF_typeForm(
        initial={'templates_for_massage': template.templates_for_massage,
                 'channel': template.channel,
                 'ntf_group': template.ntf_group})
    return render(request, "msg_sender/template_update.html",
                  {'form': form})


def subscribe(request, pk):
    global subscription
    try:
        user = User.objects.get(email=request.user)
        subscription = Subscription.objects.get(employee=user)
        notification_group = Notification_group.objects.get(id=pk)
        user.notification_group.add(notification_group)
        user.save()
        subscription.notification_group.add(notification_group)
        subscription.save()
    except:
        print("Wrong")
    return redirect('/')


def unsubscribe(request, pk):
    try:
        user = User.objects.get(email=request.user)
        subscripton = Subscription.objects.get(employee=user)
        notification_group = Notification_group.objects.get(id=pk)
        user.notification_group.remove(notification_group)
        user.save()
        subscripton.notification_group.remove(notification_group)
        subscripton.save()
    except:
        print("Wrong")
    return redirect('/')
