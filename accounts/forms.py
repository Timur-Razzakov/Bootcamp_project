from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

# from service.scraping.models import City, Speciality

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
    tg_nickname = forms.EmailField(label='Введите Имя телеграмм аккаунта, для получения уведомлений',
                                   widget=forms.EmailInput(attrs={'class': 'form-control'}))
    tg_channel = forms.EmailField(label='Введите Канал, на который хотите отправлять уведомление (тг)',
                                  widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Введите пароль ещё раз',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    send_to_email = forms.BooleanField(required=False, widget=forms.CheckboxInput,
                                       label='Получать рассылку на почту?')
    send_to_tg_channel = forms.BooleanField(required=False, widget=forms.CheckboxInput,
                                            label='Получать рассылку на канал? (тг)')
    send_to_tg_privet_channel = forms.BooleanField(required=False, widget=forms.CheckboxInput,
                                                label='Получать рассылку в личку (тг)?')

    class Meta:
        model = User
        fields = ('email', 'tg_nickname', 'tg_channel', 'password', 'password2',
                  'send_to_email', 'send_to_tg_channel', 'send_to_tg_privet_channel')

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return data['password2']


