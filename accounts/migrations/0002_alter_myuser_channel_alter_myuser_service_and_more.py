# Generated by Django 4.1 on 2022-09-04 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('msg_sender', '0002_alter_notification_ntf_group'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='channel',
            field=models.ManyToManyField(null=True, to='msg_sender.channel', verbose_name='channel_name'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='service',
            field=models.ManyToManyField(null=True, to='msg_sender.service', verbose_name='service_name'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='msg_sender.channel', verbose_name='channels'),
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='employee_requisites',
        ),
        migrations.AddField(
            model_name='subscription',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='employee'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='employee_requisites',
            field=models.ManyToManyField(to='accounts.empl_requisites'),
        ),
    ]
