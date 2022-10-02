from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from .models import Service, Notification_group, Channel, Notification, NTF_type_for_channel


class ServiceForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Service
        fields = '__all__'


class ServiceAdmin(admin.ModelAdmin):
    form = ServiceForm
    list_display = ('id', 'service_names', 'image', 'description')


class NotificationForm(forms.ModelForm):
    message = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Notification
        fields = '__all__'


class NotificationAdmin(admin.ModelAdmin):
    # form = NotificationForm
    list_display = ('id', 'created_at', 'title', 'status', 'ntf_group',
                    'url', 'message')


class Notification_groupForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Notification_group
        fields = '__all__'


class Notification_groupAdmin(admin.ModelAdmin):
    form = Notification_groupForm
    list_display = ('id', 'service_name', 'group_name', 'description')


class NTF_type_for_channelForm(forms.ModelForm):
    templates_for_massage = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = NTF_type_for_channel
        fields = '__all__'


class NTF_type_for_channelAdmin(admin.ModelAdmin):
    # form = NTF_type_for_channelForm
    list_display = ('ntf_group', 'channel', 'templates_for_massage')

    # def get_ntf_type(self, obj):
    #     return "\n".join([ntf.group_name for ntf in obj.ntf_group.all()])


class ChannelAdmin(admin.ModelAdmin):
    form = NotificationForm
    list_display = ('id', 'name')


admin.site.register(Service, ServiceAdmin)
admin.site.register(Notification_group, Notification_groupAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(NTF_type_for_channel, NTF_type_for_channelAdmin)
