# Generated by Django 4.1 on 2022-09-27 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msg_sender', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(blank=True, null=True, verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Notification Status'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='url',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='url'),
        ),
    ]
