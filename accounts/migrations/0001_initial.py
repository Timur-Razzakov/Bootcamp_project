# Generated by Django 4.1 on 2022-09-20 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('msg_sender', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('receiver', models.BooleanField(default=True)),
                ('notification_group', models.ManyToManyField(to='msg_sender.notification_group', verbose_name='notification_group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Empl_requisites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_details', models.CharField(max_length=255, verbose_name='user_requisites')),
                ('channel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='msg_sender.channel', verbose_name='channel')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='employee')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channels', models.ManyToManyField(to='msg_sender.channel')),
                ('employee_requisites', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.empl_requisites', verbose_name='employee_requisites for send')),
                ('notification_group', models.ManyToManyField(to='msg_sender.notification_group')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Message')),
                ('status', models.CharField(max_length=90, verbose_name='Notification status')),
                ('sending_status', models.CharField(blank=True, max_length=90, null=True, verbose_name='sending_status')),
                ('message_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='massage_title')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='url')),
                ('process_date', models.DateField(blank=True, null=True, verbose_name='sent_to')),
                ('created_at', models.DateField(blank=True, null=True, verbose_name='created_at')),
                ('channels', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='msg_sender.channel', verbose_name='channels for send')),
                ('employee_details', models.ManyToManyField(to='accounts.empl_requisites', verbose_name='employee_requisites')),
                ('notification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='msg_sender.notification', verbose_name='notification')),
            ],
        ),
    ]
