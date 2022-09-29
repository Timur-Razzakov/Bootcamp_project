from django.db import models


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
        return str(self.pk)


class Notification(models.Model):
    title = models.CharField(verbose_name='title', max_length=100, blank=True, null=True)
    status = models.CharField(verbose_name='Notification Status', max_length=30, blank=True, null=True)
    ntf_group = models.ForeignKey(Notification_group, verbose_name='ntf_group', on_delete=models.CASCADE,
                                  blank=True, null=True)
    url = models.CharField(verbose_name='url', max_length=30, blank=True, null=True)
    message = models.JSONField(verbose_name='Message', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=("created_at"), auto_now_add=True)
    recipient = models.TextField(verbose_name="employee_recipient", null=True, blank=True)
    processing_status = models.BooleanField(verbose_name="processing_status", default=False)

    def __str__(self):
        return self.title


class NTF_type_for_channel(models.Model):
    ntf_group = models.ForeignKey(Notification_group, verbose_name='ntf_group', on_delete=models.CASCADE, null=True, blank=True)
    channel = models.ForeignKey(Channel, verbose_name='channel', on_delete=models.CASCADE, null=True,
                                blank=True)
    templates_for_massage = models.TextField(verbose_name='templates_for_massage')

    def __str__(self):
        return str(self.channel)
