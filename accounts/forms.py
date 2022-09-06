from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

from msg_sender.models import Channel, Service
from .models import Empl_requisites, Subscription

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
    channel = forms.ModelChoiceField(
        queryset=Channel.objects.all(),
        to_field_name="channels",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Выберите каналы, на которые хотите получать уведомления'
    )
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        to_field_name="service_names",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Выберите сервис, от которого хотите получать уведомления'
    )
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Введите пароль ещё раз',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    receiver = forms.BooleanField(required=False, widget=forms.CheckboxInput,
                                  label='Хотите ли вы получать уведомления?')

    # send_to_email = forms.BooleanField(required=False, widget=forms.CheckboxInput,
    #                                    label='Получать рассылку на почту?')
    # send_to_tg_channel = forms.BooleanField(required=False, widget=forms.CheckboxInput,
    #                                         label='Получать рассылку на канал? (тг)')
    # send_to_tg_privet_channel = forms.BooleanField(required=False, widget=forms.CheckboxInput,
    #                                                label='Получать рассылку в личку (тг)?')
    class Meta:
        model = User
        fields = ('email', 'channel', 'service', 'password', 'password2', "receiver",)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return data['password2']


"""Форма для получения реквизитов пользователя"""


class UserRequisitesForm(forms.ModelForm):

    # employee = forms.ModelChoiceField(
    #     queryset=User.objects.filter(is_active=True),
    #     required=True,
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     label='employee_email'
    # )
    tg_nickname = forms.CharField(label='Введите Имя телеграмм аккаунта, для получения уведомлений',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    tg_channel = forms.CharField(label='Введите Канал, на который хотите получать уведомление (тг)',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(
        label='Введите номер телефона, на который хотите получать уведомление (тг)',
        widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Empl_requisites
        fields = ('tg_nickname', 'tg_channel', 'phone_number')  # 'employee',


"""Форма для заполнения подписки на сервисы"""

#
# class SubscriptionForm(forms.Form):
#     """создаём форму для подписки"""
#     service_name = forms.ModelMultipleChoiceField(
#         queryset=Subscription.objects.all(),
#         required=True,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#
#     class Meta:
#         model = Subscription
#         fields = ('employee', 'service_name', 'channel', 'employee_requisites',)
