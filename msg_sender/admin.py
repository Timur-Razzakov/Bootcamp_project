from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms
from django.template.defaultfilters import truncatechars
from .models import Service, Notification_group, Channel, Notification, NTF_type_for_channel
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ServiceForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Service
        fields = '__all__'


class ServiceAdmin(admin.ModelAdmin):
    form = ServiceForm
    list_display = ('name', 'image', 'description')


class NotificationForm(forms.ModelForm):
    message = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Notification
        fields = '__all__'


class NotificationAdmin(admin.ModelAdmin):
    form = NotificationForm
    list_display = ('title', 'status', 'channel_name',
                    'ntf_group', 'url', 'receiver', 'message', 'created_at')


admin.site.register(Service, ServiceAdmin)
admin.site.register(Notification_group)
admin.site.register(Channel)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(NTF_type_for_channel)
