from django import forms

from .models import Notification, Notification_group, Service


class NotificationForm(forms.Form):
    """создаём форму для уведолений"""
    ntf_group = forms.ModelChoiceField(
        queryset=Notification_group.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Notification
        fields = ('title', 'status', 'message', 'ntf_group', 'created_at', 'email', 'url',)
