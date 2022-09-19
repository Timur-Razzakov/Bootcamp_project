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
# TODO: разобраться с разделением листа с реквизитами и отправка
# -------------------------------------------------------------------------------
import logging
from aiogram.types import message
from aiogram import Bot, Dispatcher, executor, types
from accounts.models import Result, Empl_requisites
from msg_sender.models import Channel
from django.core.management.base import BaseCommand
# задаём уровень логов
logging.basicConfig(level=logging.INFO)
from icecream import ic

bot = Bot(token=os.environ.get('BOT_TOKEN'))
dp = Dispatcher(bot)
admins = 99169335


# channels = Channel.objects.filter(name__startswith='telegram').values('pk')
# for item in channels:
#     qs = Result.objects.filter(channels=item['pk']).exclude(sending_status='Ok').values(
#         'employee_details', 'status', 'sending_status', 'message_title',
#         'url', 'process_date', 'created_at', 'channels',
#         'message')
#     CHAT_ID = []
#     data_send = []
#     for item in qs:
#         employee_req = Empl_requisites.objects.filter(id=item['employee_details'])
#         message_text = "<h1>{title}</h1>\n" \
#                        "<p>{message}</p>\n" \
#                        "<p>{status}</p>\n" \
#                        "<p>{created_at}</p>\n".format(title=item['message_title'],
#                                                       message=item['message'], status=item['status'],
#                                                       created_at=item['created_at']
#                                                       )
#         for details in employee_req:
#             CHAT_ID.append(details)
#         data_send.append(message_text)

@dp.message_handler(commands=['sendall'])
async def sendall(message: types.Message):
    command_sendall = message.from_user.id
    if message.chat.id == admins:
        await message.answer(('start'))
        for id in CHAT_ID:
            for text in data_send:
                await bot.send_message(id,text)
        await message.answer('Done!!')
    else:
        await message.answer('error!!')
    # async def sendall(message: types.Message):
    #     for details in employee_req:
    #         if details == 99169335:
    #             text = message_text
    #             await bot.send_message(details, text)  # send to user
    #

#
    #     @dp.message_handler(commands=['sendall'])
    #     def notify(message):
    #         command_sendall= message.from_user.id
    #         if command_sendall in admins:
    #             for details in employee_req:
    #                 try:
    #                     bot.send_message(details, message_text)  # send to user
    #                 except Exception as e:
    #                     bot.send_message(command_sendall, f'ошибка отправки сообщения юзеру - {details}')
    #         else:
    #             bot.send_message(command_sendall, f'у вас нет прав для запуска команды')
    # if __name__ == "__main__":
    #     try:
    #         bot.polling(none_stop=True)
    #     except Exception as e:
    #         pass

#
#     # await message.answer(message.text)
#     await bot.send_message(99169335, 'hello') # send to user
# if __name__ == '__main__':
#     executor.start_polling(dp,skip_updates=True)
#
# """postcode = '12345'
# Address.objects.extra(where=["%s LIKE postcode_prefix||'%%'"], params=[postcode])"""
#
#
#
# message = {'message_title': item['message_title'],
#            'message': item['message'],
#            'status': item['status'],
#            'created_at': item['created_at'],
#            'url': item['url'],
#            }
# # def get_data():
# global send_msg, CHAT_ID
# channels = Channel.objects.filter(name__startswith='telegram').values('pk')
# for item in channels:
#     qs = Result.objects.filter(channels=item['pk']).exclude(sending_status='Ok').values(
#         'employee_details', 'status', 'sending_status', 'message_title',
#         'url', 'process_date', 'created_at', 'channels',
#         'message')
#     CHAT_ID = []
#     data_send = []
#     for item in qs:
#         employee_req = Empl_requisites.objects.filter(id=item['employee_details'])
#         message_text = "<h2>{title}</h2>\n" \
#                        "<p>{message}</p>\n" \
#                        "<p>{status}</p>\n" \
#                        "<p>{created_at}</p>\n".format(title=item['message_title'],
#                                                       message=item['message'], status=item['status'],
#                                                       created_at=item['created_at']
#                                                       )
#         ic(message_text)
#
#
#         @dp.message_handler(commands=['sendall'])
#         async def sendall(message: types.Message):
#             if message.chat.type == 'private':
#                 text = message_text
#                 users = CHAT_ID
#                 for id in users:
#                     try:
#                         await bot.send_message(id, text)  # send to user
#                     except:
#                         pass
        # data_send.append(user_data)
        #     for details in employee_req:
        #         CHAT_ID.append(details)
        # send_msg(text=data_send, token=bot, chat_id=CHAT_ID)
#
# def send_msg(text, token, chat_id):
#     url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
#     return requests.get(url_req)
# def user_data(message_title, message, status,created_at,url):
#     message_text = "<h2>{title}</h2>\n" \
#                 "<p>{message}</p>\n" \
#                 "<p>{status}</p>\n" \
#                 "<p>{created_at}</p>\n".format(title=message_title,
#                        message=message,status=status,created_at=created_at
#                        )
#     return message_text


# @dp.message_handler(commands=['sendall'])
# async def sendall(message: types.Message):
#     if message.chat.type == 'private':
#         if message.from_user.id == CHAT_ID:
#             text = message.text = data
#             users = CHAT_ID
#             for id in users:
#                 try:
#                     await bot.send_message(id, text) # send to user
#                 except:
#                     pass


#     #     send_msg(text=data,token=TOKEN, chat_id=CHAT_ID)
#     #
#     # def send_msg(text, token, chat_id):
#     #     url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
#     #     ic(url_req)
#     #     return requests.get(url_req)
# message_text = f"""<div class="container">
#     <div class="row">
#          <div class="col-md-4">
#             <h2>{title}</h2>
#             <p>{message}</p>
#             <p><a class="btn btn-secondary" href="{}" role="button">{}</a></p>
#         </div>
#     </div>
#   </div>""".format(title=item['message_title'])
