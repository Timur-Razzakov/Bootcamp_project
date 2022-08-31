from django.db import models
from django.conf import settings
from django.core import validators


class Service(models.Model):
    name = models.CharField(verbose_name='service_name', max_length=255)
    description = models.CharField(verbose_name='description', max_length=255)
    how_can_send = models.CharField(verbose_name='how_can_send', max_length=255)

    def __str__(self):
        return self.name


class Notification(models.Model):
    title = models.CharField(verbose_name='title', max_length=100)
    service_name = models.ForeignKey(Service, verbose_name='service', on_delete=models.CASCADE, blank=True)
    message = models.CharField(verbose_name='Message', max_length=100)

    status = models.CharField(verbose_name='Notification Status', max_length=15)

    created_at = models.DateTimeField(verbose_name=("created_at"), auto_now_add=True)
    receiver = models.CharField(verbose_name= ('Receiver FCM Token'), max_length=100)


def __str__(self):
    return self.message
