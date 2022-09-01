# Generated by Django 4.1 on 2022-09-01 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_name', models.CharField(max_length=255, verbose_name='channel')),
            ],
        ),
        migrations.CreateModel(
            name='Notification_group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='description_ntf')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='service_name')),
                ('image', models.ImageField(blank=True, upload_to='media/%Y/%m/%d', verbose_name=' images')),
                ('description', models.CharField(max_length=255, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='NTF_type_for_channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('templates_for_massage', models.CharField(max_length=255, verbose_name='templates_for_massage')),
                ('channel', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='msg_sender.channel', verbose_name='channel')),
                ('ntf_group', models.ManyToManyField(to='msg_sender.notification_group')),
            ],
        ),
        migrations.AddField(
            model_name='notification_group',
            name='service_name',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='msg_sender.service', verbose_name='service'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('message', models.CharField(max_length=255, verbose_name='Message')),
                ('status', models.CharField(max_length=30, verbose_name='Notification Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('url', models.CharField(max_length=30, verbose_name='url')),
                ('receiver', models.CharField(max_length=100, verbose_name='Receiver FCM Token')),
                ('channel_name', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='msg_sender.channel', verbose_name='channel_name')),
                ('ntf_group', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='msg_sender.notification_group', verbose_name='channel_name')),
            ],
        ),
    ]
