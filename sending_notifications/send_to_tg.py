import os
import sys

import schedule
from icecream import ic

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "natification_service.settings")
import django

django.setup()

# -------------------------------------------------------------------------------
import datetime
import os, sys

import requests

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "natification_service.settings")
import django

django.setup()
# -------------------------------------------------------------------------------
import logging
from aiogram import Bot, Dispatcher
from accounts.models import Result
from msg_sender.models import Channel

# задаём уровень логов
logging.basicConfig(level=logging.INFO)

token = os.environ.get('BOT_TOKEN')

bot = Bot(token=os.environ.get('BOT_TOKEN'))
dp = Dispatcher(bot)

"""Функция для отправки нотификаций по телеграмму"""


def sent_ntf():
    channel = Channel.objects.get(name='Telegram')
    # Обращаемся в таблицу за новыми results по коду статус и по каналу связи
    results = Result.objects.filter(channels=channel).exclude(sending_status='1')
    ic(results)
    print('Данные не найдены...')
    for result in results:
        ic(result)
        employee_details = result.employee_details.all()  # Из results извлекаем реквизиты
        ic(employee_details)
        for detail in employee_details:
            params = {
                "chat_id": detail,
                "text": result.message,
                "parse_mode": "HTML"
            }
            ic(params)
            url_req = "https://api.telegram.org/bot" \
                      + token + "/sendMessage"
            reg = requests.get(url_req, params=params)
            ic(reg)
        # Проверка отправки
        if reg:  # Если успешно, статус-1
            result.sending_status = '1'
            result.process_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            result.save()
            print("Sended")
        else:  # Если ошибка, статус-2
            result.sending_status = '2'
            result.process_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            result.save()
            print("Not sended")


# Планировшик
def main():
    schedule.every(5).seconds.do(sent_ntf)
    # schedule.every(5).minutes.do(sent_ntf)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
