import re

from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from icecream import ic

from msg_sender.models import Channel, Notification_group
from .models import Empl_requisites

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    """ Проверка на валидацию"""

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя нет!')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Пароль не верный!')
            # проверяем существует ли пользователь
            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError('Данный аккаунт отключен')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Введите email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    notification_group = forms.ModelMultipleChoiceField(
        queryset=Notification_group.objects.all(),
        to_field_name="group_name",
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),  #
        label='Выберите группу нотификации, от которой хотите получать уведомления'
    )
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Введите пароль ещё раз',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    receiver = forms.BooleanField(required=False, widget=forms.CheckboxInput,
                                  label='Хотите ли вы получать уведомления?')

    class Meta:
        model = User
        fields = ('email', 'notification_group', 'password', 'password2', "receiver",)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return data['password2']


"""Форма для получения реквизитов пользователя"""


class UserRequisitesForm(forms.ModelForm):
    channel = forms.ModelChoiceField(
        queryset=Channel.objects.all(),
        to_field_name="name",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Выберите канал, для которого хотите ввести реквизиты'
    )
    user_details = forms.CharField(label='Введите свои реквизиты, через запятую.'
                                         ' Если вы хотите получать через телеграмм,то введите свой channelID, '
                                         'его можете найти с помощью "@username_to_id_bot" этого бота.'
                                         'Или введите ссылку канала, группы',
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Empl_requisites
        fields = ('channel', 'user_details')  # 'employee',

    """Проверяем есть ли реквизиты и производим проверку,
        на верность указанных данных, относительно канала"""

    def clean(self, *args, **kwargs):
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
        channels = self.cleaned_data.get('channel')
        user_details = self.cleaned_data.get('user_details').split(',')
        if user_details:
            for item in user_details:
                if channels.name == 'Email' and re.match(pattern, item.strip()) is not None \
                        or channels.name.startswith('Telegram') and item[1:].isdigit():
                    qs = Empl_requisites.objects.filter(user_details=item).exclude(
                        user_details__startswith='-')
                    if qs.exists():
                        raise forms.ValidationError('Реквизиты существуют')
                else:
                    raise forms.ValidationError('Реквизиты не соответствуют  '
                                                'указанному каналу!!')
            return super(UserRequisitesForm, self).clean(*args, **kwargs)


"""
Форма для обновления указанных данных пользователем
"""


class UserRequisitesUpdateForm(forms.Form):
    employee = forms.EmailField()
    channel = forms.CharField()
    user_details = forms.CharField()

    """Проверяем есть ли реквизиты и производим проверку,
          на верность указанных данных, относительно канала"""

    def clean(self, *args, **kwargs):
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
        channels = self.cleaned_data.get('channel')
        user_details = self.cleaned_data.get('user_details').split(',')
        if user_details:
            for item in user_details:
                ic(item)
                if channels.name == 'Email' and re.match(pattern, item) is not None \
                        or channels.name.startswith('Telegram') and item.isdigit():

                    qs = Empl_requisites.objects.filter(user_details=item).exclude(
                        user_details__startswith='-')
                    if qs.exists():
                        raise forms.ValidationError('Реквизиты существуют')
                else:
                    ic(item)
                    raise forms.ValidationError('Реквизиты не соответствуют  '
                                                'указанному каналу!!')
            return super(UserRequisitesUpdateForm, self).clean(*args, **kwargs)


class UserUpdateForm(UserRegistrationForm):
    current_password = forms.CharField(label='Введите текущий пароль',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Введите пароль ещё раз',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    field_order = ('email', 'channel', 'notification_group', 'current_password',
                   'password', 'password2', 'receiver')

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return data['password2']
