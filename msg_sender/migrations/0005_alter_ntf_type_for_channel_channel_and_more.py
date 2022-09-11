# Generated by Django 4.1 on 2022-09-11 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msg_sender', '0004_remove_ntf_type_for_channel_channel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ntf_type_for_channel',
            name='channel',
            field=models.ManyToManyField(blank=True, null=True, to='msg_sender.channel', verbose_name='channel'),
        ),
        migrations.AlterField(
            model_name='ntf_type_for_channel',
            name='ntf_group',
            field=models.ManyToManyField(blank=True, null=True, to='msg_sender.notification_group'),
        ),
    ]
