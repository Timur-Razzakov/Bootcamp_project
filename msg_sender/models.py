from django.db import models
from django.conf import settings
from django.core import validators


class Service(models.Model):
    service_names = models.CharField(verbose_name='service_name', max_length=255)
    image = models.ImageField(verbose_name=' images', upload_to='media/%Y/%m/%d', blank=True)
    description = models.TextField(verbose_name='description', max_length=255,null=True,blank=True)

    def __str__(self):
        return self.service_names


class Channel(models.Model):
    channels = models.CharField(verbose_name='channel', max_length=255)

    def __str__(self):
        return self.channels
#TODO : переименовать description на group_name

class Notification_group(models.Model):
    service_name = models.ForeignKey(Service, verbose_name='service', on_delete=models.CASCADE, blank=True)
    description = models.CharField(verbose_name='description_ntf', max_length=255)
    # group_name = models.CharField(verbose_name='description_ntf', max_length=255)

    def __str__(self):
        return self.description


class Notification(models.Model):
    title = models.CharField(verbose_name='title', max_length=100)
    status = models.CharField(verbose_name='Notification Status', max_length=30)
    ntf_group = models.ForeignKey(Notification_group, verbose_name='service_name', on_delete=models.CASCADE,
                                  blank=True, null=True)
    email = models.EmailField(verbose_name='email address', max_length=255,
                              unique=True, )

    url = models.CharField(verbose_name='url', max_length=30)
    message = models.CharField(verbose_name='Message', max_length=255)
    created_at = models.DateTimeField(verbose_name=("created_at"), auto_now_add=True)

    def get_channel_names(self, obj):
        return "\n".join([p.channels for p in self.channel_name.all()])

    def __str__(self):
        return self.title


class NTF_type_for_channel(models.Model):
    templates_for_massage = models.CharField(verbose_name='templates_for_massage', max_length=255)
    ntf_group = models.ManyToManyField(Notification_group)
    channel = models.ForeignKey(Channel, verbose_name='channel', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return str(self.ntf_group)
