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

# задаём уровень логов
logging.basicConfig(level=logging.INFO)
from icecream import ic

token = os.environ.get('BOT_TOKEN')

bot = Bot(token=os.environ.get('BOT_TOKEN'))
dp = Dispatcher(bot)

channels = Channel.objects.filter(name__startswith='telegram').values('pk')
for item in channels:
    qs = Result.objects.filter(channels=item['pk']).exclude(sending_status='Ok').values(
        'employee_details', 'sending_status','process_date','message')
    for empl_item in qs:
        empl = Empl_requisites.objects.get(id=empl_item['employee_details'])
        params = {
            "chat_id": empl.user_details,
            "text": empl_item['message'],
            "parse_mode": "HTML"
        }
        ic(params)
        url_req = "https://api.telegram.org/bot" \
                      + token + "/sendMessage"
        req = requests.get(url_req, params=params)
        ic(req.text)

    #
    # for empl_item in qs:
    #     message_text = f"<b>{empl_item['message_title']}</b>\n\n" \
    #                    f"<em style='color:red'><b>Cтатус:</b> {empl_item['status']}</em>\n\n" \
    #                    f"<b>{empl_item['message']}</b>\n" \
    #                    f"<b>{empl_item['created_at']}</b>\n" \
    #                    f"<a href='{empl_item['url']}'>{empl_item['url']}</a>\n"
    #     empl = Empl_requisites.objects.get(id=empl_item['employee_details'])
    #     # data.append({"chat_id": empl.user_details, "message": message_text})
    #     params = {
    #         "chat_id": empl.user_details,
    #         "text": message_text,
    #         "parse_mode": "HTML"
    #     }
    #     url_req = "https://api.telegram.org/bot" \
    #               + token + "/sendMessage"
    #     req = requests.get(url_req, params=params)
    # ic(req.text)

