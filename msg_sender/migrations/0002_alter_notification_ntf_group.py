# Generated by Django 4.1 on 2022-09-03 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('msg_sender', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='ntf_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='msg_sender.notification_group', verbose_name='service_name'),
        ),
    ]
