import datetime
import json
import os, sys

import requests

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from telegram.utils.request import Request

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "natification_service.settings")
import django

django.setup()
# TODO: разобраться с разделением листа с реквизитами и отправка
# -------------------------------------------------------------------------------
import datetime
import json
import os, sys

import requests

from django.contrib.auth import get_user_model

from telegram.utils.request import Request

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "natification_service.settings")
import django

django.setup()
# -------------------------------------------------------------------------------
import logging
from aiogram import Bot, Dispatcher, executor, types
from accounts.models import Result, Empl_requisites
from msg_sender.models import Channel
from icecream import ic
# задаём уровень логов
logging.basicConfig(level=logging.INFO)

token = os.environ.get('BOT_TOKEN')

bot = Bot(token=os.environ.get('BOT_TOKEN'))
dp = Dispatcher(bot)



def handle(data, result):
    subject = data['subject']
    content = data['message']
    from_email = ADMIN_USER
    to_send = data['employee_details']
    msg = EmailMessage(subject, content, from_email, to_send)
    res = msg.send()
    result.sending_status = 'Ok'
    result.process_date = datetime.date.today()
    result.save()
    print("Sended")


for result in results:
    employee_details = result.employee_details.all()
    deteils_list = []
    for detail in employee_details:
        deteils_list.append(str(detail))

    data = {'subject': result.notification.title,
            'message': result.message,
            'employee_details': deteils_list
            }

    handle(data, result)

for item in results:
    ic(item.message)
def sent_ntf():
    for empl_item in results:
        empl = Empl_requisites.objects.get(id=empl_item['employee_details'])
        empl_item['process_date'] = datetime.date.today()
        # empl_item.save()
        params = {
            "chat_id": empl.user_details,
            "text": empl_item['message'],
            "parse_mode": "HTML"
        }
        # url_req = "https://api.telegram.org/bot" \
        #           + token + "/sendMessage"
        # reg = requests.get(url_req, params=params)

sent_ntf()

# if reg:
#     empl_item['sending_status'] = '1'
# else:
#     empl_item['sending_status'] = '2'
# empl_item.save()