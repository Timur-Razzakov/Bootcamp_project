from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from msg_sender.models import  Channel, NTF_type_for_channel,Notification_group


# class Employee(models.Model):
#     email = models.EmailField(max_length=256, verbose_name='почта')
#     service = models.ManyToManyField(Service)
#     receiver = models.BooleanField(max_length=50, verbose_name='want_to_receive', null=True)
#     password = models.CharField(max_length=256, verbose_name='password')
#     repeat_password = models.CharField(max_length=256, verbose_name='repeat-password')
#
#     def __str__(self):
#         return self.email


class Empl_requisites(models.Model):
    employee = models.ForeignKey('MyUser', verbose_name='employee', on_delete=models.CASCADE,unique=True, blank=True)
    tg_nickname = models.CharField(max_length=50, verbose_name='tg_nickname', null=True)
    tg_channel = models.CharField(max_length=50, verbose_name='tg_channel', null=True)
    phone_number = models.CharField(max_length=50, verbose_name='phone_number', null=True)

    def __str__(self):
        return self.phone_number


class Subscription(models.Model):
    employee = models.ForeignKey('MyUser', verbose_name='employee', on_delete=models.SET_NULL, null=True,
                                 blank=True)
    notification_group = models.ManyToManyField(Notification_group)
    channel = models.ManyToManyField(Channel)
    employee_requisites = models.ManyToManyField(Empl_requisites)
    # service_name = models.ForeignKey(Service, verbose_name='service_name', on_delete=models.CASCADE,
    #                                  null=True,
    #                                  blank=True)
    # employee_requisites = models.ForeignKey(Empl_requisites, verbose_name='employee_requisites',
    #                                         on_delete=models.CASCADE, null=True,
    #                                         blank=True)
    def __str__(self):
        return str(self.employee)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Создаёт пользователя с указанным email-лом и паролем
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)  # зашифровывает пароль
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Создаёт супер пользователя для доступа к админке
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    notification_group = models.ManyToManyField(Notification_group, verbose_name='notification_group')

    channel = models.ManyToManyField(Channel, verbose_name='channel_name')
    # channel = models.ForeignKey(Channel, verbose_name='channel_name', on_delete=models.SET_NULL, null=True,
    #                             blank=True)
    # notification_group = models.ForeignKey(Notification_group, verbose_name='notification_group', on_delete=models.SET_NULL, null=True,
    #                             blank=True)
    receiver = models.BooleanField(default=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """проверяет есть ли у пользователя указанное разрешение """
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """есть  ли у пользователя разрешение на доступ к моделям в данном приложении. """
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """ Является ли пользователь администратором """
        # Simplest possible answer: All admins are staff
        return self.is_admin
