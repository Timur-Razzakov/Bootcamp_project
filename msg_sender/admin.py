from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms
from django.template.defaultfilters import truncatechars
from .models import Service, Notification_group, Channel, Notification, NTF_type_for_channel




admin.site.register(Service)
admin.site.register(Notification_group)
admin.site.register(Channel)
admin.site.register(Notification)
admin.site.register(NTF_type_for_channel)

