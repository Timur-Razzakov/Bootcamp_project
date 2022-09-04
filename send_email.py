import datetime
import os,sys
from django.contrib.auth import get_user_model
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] ="natification_service.settings"

import django
django.setup()

# -------------------------------------------------------------------------------

import time
from django.core.mail import EmailMultiAlternatives
from msg_sender.models import Notification,Service
from accounts.models import Empl_requisites,MyUser
from natification_service.settings import (
    EMAIL_HOST_USER
)

today = datetime.date.today()
subject = f"Нотификация {today}"
text_content = f"Пробная нотификация {today}"
empty = '<h2> упс... </h2>'

# ADMIN_USER = EMAIL_HOST_USER
#
# # Возвращает пользователя по умолчанию
User = get_user_model()
#
qs = Notification.objects.filter(url='some url')
print(qs)
# #
# qs = Employee.objects.filter(receiver=True).values('channel', 'service', 'email')
# print(User.objects.all())
    # user_dct = {}
    # for item in qs:
    #     user_dct.setdefault((item['city'], item['speciality']), [])  # 3параметр, это тип (список)
    #     user_dct[(item['city'], item['speciality'])].append(item['email'])
    #
    # if user_dct:
    #     # поиск всех значений, которые принадлежат данной паре
    #     params = {'city_id__in': [], 'speciality_id__in': []}
    #
    #     for pair in user_dct.keys():
    #         params['city_id__in'].append(pair[0])
    #         params['speciality_id__in'].append(pair[1])
    #     qs = Vacancies.objects.filter(**params).values()[:10]
    #     vacancy = {}
    #     for item in qs:
    #         """Получем значения из нашего 'queryset' """
    #         vacancy.setdefault((item['city_id'], item['speciality_id']), [])
    #         vacancy[(item['city_id'], item['speciality_id'])].append(item)
    #     for keys, emails in user_dct.items():
    #         rows = vacancy.get(keys, [])
    #         html = ''
    #         for row in rows:
    #             """Формат для  отправки сообщения"""
    #             html += f'<h5><a href="{row["url"]}">{row["title"]}</a></h5>'
    #             html += f'<p><strong>{row["salary"]}</strong></p>'
    #             html += f'<p><strong>{row["company_name"]}</strong></p>'
    #         _html = html if html else empty
    #         for email in emails:
    #             """Перебираем все наши имайли и отправляем сообщения"""
    #             to = email
    #             msg = EmailMultiAlternatives(
    #                 subject, text_content, ADMIN_USER, [to]
    #             )
    #             msg.attach_alternative(_html, "text/html")
    #             msg.send()
    #
