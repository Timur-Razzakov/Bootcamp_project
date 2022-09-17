from django.db import models
from django.conf import settings
from django.core import validators



class Service(models.Model):
    service_names = models.CharField(verbose_name='service_name', max_length=255)
    image = models.ImageField(verbose_name=' images', upload_to='media/%Y/%m/%d', blank=True)
    description = models.TextField(verbose_name='description', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.service_names


class Channel(models.Model):
    name = models.CharField(verbose_name='channel_name', max_length=255)

    def __str__(self):
        return self.name


class Notification_group(models.Model):
    service_name = models.ForeignKey(Service, verbose_name='service', on_delete=models.CASCADE, null=True,
                                     blank=True)
    group_name = models.CharField(verbose_name='group_name', max_length=255)
    description = models.TextField(verbose_name='description_ntf_group', max_length=255)

    def __str__(self):
        return self.group_name


class Notification(models.Model):
    title = models.CharField(verbose_name='title', max_length=100)
    status = models.CharField(verbose_name='Notification Status', max_length=30)
    ntf_group = models.ForeignKey(Notification_group, verbose_name='ntf_group', on_delete=models.CASCADE,
                                  blank=True, null=True)
    url = models.CharField(verbose_name='url', max_length=30)
    message = models.TextField(verbose_name='Message', max_length=255)
    created_at = models.DateField(verbose_name=("created_at"), auto_now_add=True)
    recipient = models.CharField(verbose_name="employee_recipient",max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title


class NTF_type_for_channel(models.Model):
    ntf_group = models.ManyToManyField(Notification_group, blank=True)
    channel = models.ManyToManyField(Channel, verbose_name='channel', blank=True)
    templates_for_massage = models.TextField(verbose_name='templates_for_massage')

    def __str__(self):
        return self.templates_for_massage
