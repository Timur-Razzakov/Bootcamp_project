from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import Notification, Notification_group, NTF_type_for_channel, Channel


class NotificationForm(forms.Form):
    """создаём форму для уведомлений"""
    ntf_group = forms.ModelChoiceField(
        queryset=Notification_group.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Notification
        fields = ('title', 'status', 'message', 'ntf_group', 'created_at' 'url',)


"""Форма для шаблонов от пользователя"""


class NTF_typeForm(forms.ModelForm):
    ntf_group = forms.ModelMultipleChoiceField(
        label='Выберите группу нотификации, для который хотите добавить шаблон',
        queryset=Notification_group.objects.all().values('group_name'),
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    channel = forms.ModelChoiceField(
        queryset=Channel.objects.all(),
        to_field_name="name",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Выберите канал,для которого хотите добавить шаблон'
    )
    templates_for_massage = forms.CharField(
        widget=CKEditorWidget(attrs={'class': 'form-control'}),
        label='Ваш шаблон'
    )

    class Meta:
        model = NTF_type_for_channel
        fields = ('ntf_group', 'channel', 'templates_for_massage')
