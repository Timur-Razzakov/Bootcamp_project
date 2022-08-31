from django.db import models
from django.conf import settings
from django.core import validators


class Service(models.Model):
    name = models.CharField(verbose_name='service_name', max_length=255)
    description = models.CharField(verbose_name='description', max_length=255)

    def __str__(self):
        return self.name


class Notification_group(models.Model):
    service_name = models.ForeignKey(Service, verbose_name='service', on_delete=models.CASCADE, blank=True)
    description = models.CharField(verbose_name='description_ntf', max_length=255)

    def __str__(self):
        return self.service_name


class Channel(models.Model):
    channel_name = models.CharField(verbose_name='channel', max_length=255)

    def __str__(self):
        return self.channel_name


class Notification(models.Model):
    title = models.CharField(verbose_name='title', max_length=100)
    message = models.CharField(verbose_name='Message', max_length=255)
    status = models.CharField(verbose_name='Notification Status', max_length=30)
    created_at = models.DateTimeField(verbose_name=("created_at"), auto_now_add=True)
    channel_name = models.ForeignKey(Channel, verbose_name='channel_name', on_delete=models.CASCADE, blank=True)
    url = models.CharField(verbose_name='url', max_length=30)
    ntf_group = models.ForeignKey(Notification_group, verbose_name='channel_name', on_delete=models.CASCADE, blank=True)
    receiver = models.CharField(verbose_name= ('Receiver FCM Token'), max_length=100)

    def __str__(self):
        return self.title

class NTF_type_for_channel(models.Model):
    templates_for_massage = models.CharField(verbose_name='templates_for_massage', max_length=255)
    ntf_group = models.ManyToManyField(Notification_group)

    channel = models.ForeignKey(Channel,verbose_name='channel', on_delete=models.CASCADE, blank=True)
    def __str__(self):
        return self.templates_for_massage