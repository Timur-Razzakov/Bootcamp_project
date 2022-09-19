# import datetime
# import json
import os, sys

import psycopg2
import requests

from django.contrib.auth import get_user_model
from icecream import ic

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "natification_service.settings")
import django

django.setup()
# # TODO: разобраться с разделением листа с реквизитами и отправка
# # -------------------------------------------------------------------------------


from accounts.models import Result, Empl_requisites
from msg_sender.models import Channel

# # Подключаемся к PostgreSQL
# conn = psycopg2.connect(dbname=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'),
#                         password=os.environ.get('POSTGRES_PASSWORD'), host=os.environ.get('POSTGRES_HOST'))
# cursor = conn.cursor()

# объявляем массив сообщений и CHAT_ID
CHAT_ID = []
data_send = []
#получаем нужные данные
channels = Channel.objects.filter(name__startswith='telegram').values('pk')
for item in channels:
    qs = Result.objects.filter(channels=item['pk']).exclude(sending_status='Ok').values(
        'employee_details', 'status', 'sending_status', 'message_title',
        'url', 'process_date', 'created_at', 'channels',
        'message')
    for item in qs:
        employee_req = Empl_requisites.objects.filter(id=item['employee_details'])
        message_text = "<h2>{title}</h2>\n" \
                       "<p>{message}</p>\n" \
                       "<p>{status}</p>\n" \
                       "<p>{created_at}</p>\n".format(title=item['message_title'],
                                                      message=item['message'], status=item['status'],
                                                      created_at=item['created_at']
                                                      )
        for details in employee_req:
            CHAT_ID.append(details)
        data_send.append(message_text)
ic(CHAT_ID)