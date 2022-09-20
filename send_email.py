import datetime
import os, sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "natification_service.settings")
import django

django.setup()

# -------------------------------------------------------------------------------

from django.core.mail import EmailMessage
from msg_sender.models import Channel, NTF_type_for_channel

from accounts.models import Result
from natification_service.settings import (
    EMAIL_HOST_USER
)

ADMIN_USER = EMAIL_HOST_USER
#
# # Возвращает пользователя по умолчанию
User = get_user_model()

channel = Channel.objects.get(name='email')
results = Result.objects.filter(channels=channel).exclude(sending_status='Ok')
ntf_templates = NTF_type_for_channel.objects.get(channel=channel)


def handle(data, result):
    subject = data['message_title']
    content = ntf_templates.templates_for_massage.format(status=data['status'],
                                                        message_title=data['message_title'],
                                                        message=data['message'],
                                                        url=data['url'],
                                                        created_at=data['created_at'])
    print(content)
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

    data = {'message_title': result.message_title,
            'message': result.message,
            'status': result.status,
            'created_at': str(result.created_at),
            'url': result.url,
            'employee_details': deteils_list
            }

    handle(data, result)
