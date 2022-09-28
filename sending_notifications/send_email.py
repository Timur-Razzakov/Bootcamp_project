import schedule
from datetime import datetime
import os, sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "natification_service.settings")
import django

django.setup()

# -------------------------------------------------------------------------------

from django.core.mail import EmailMessage
from msg_sender.models import Channel

from accounts.models import Result
from natification_service.settings import (
    EMAIL_HOST_USER
)

ADMIN_USER = EMAIL_HOST_USER
#
# # Возвращает пользователя по умолчанию
User = get_user_model()


def handle():
    channel = Channel.objects.get(name='Email')
    # Обращаемся в таблицу за новыми results по коду статус и по каналу связи
    results = Result.objects.filter(channels=channel).exclude(sending_status='1')
    # Тут перебираем каждую строку result и отправляем по отдельности
    for result in results:
        employee_details = result.employee_details.all()  # Из results извлекаем реквизиты

        # Реквизиты записываем в список в виде строки, потому что EmailMessage в получатели принимает по списку
        details = []
        for detail in employee_details:
            details.append(str(detail))

            # Тут создаем аргументы для EmailMessage
        subject = result.created_at
        # subject = result.notification.message_title
        content = result.message
        from_email = ADMIN_USER
        to_send = details

        # Создаем экземпляр класса EmailMessage
        msg = EmailMessage(subject, content, from_email, to_send)
        msg.content_subtype = "HTML"
        res = msg.send()  # Отправляем

        # Проверка отправки
        if res:  # Если отправится изменяем статус на 1
            result.sending_status = '1'
            result.process_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            result.save()
            print("Sended")
        else:  # Если не отправится изменяем статус на 2
            result.sending_status = '2'
            result.process_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            result.save()
            print("Not sended")


def main():
    # Это планировшик, он каждый n секунд(seconds)/минут(minutes) сможет запускать код
    schedule.every(5).seconds.do(handle)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
