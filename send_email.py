import datetime

import os, sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "natification_service.settings")
import django

django.setup()

# -------------------------------------------------------------------------------
import json
import time
from django.core.mail import EmailMultiAlternatives, EmailMessage
from msg_sender.models import Notification, Service, Result, Channel
from accounts.models import Empl_requisites, MyUser
from natification_service.settings import (
    EMAIL_HOST_USER
)

from msg_sender.views import ADMIN_USER
from django.template.loader import render_to_string

results = Result.objects.filter(channels=Channel.objects.get(name='email')).exclude(sending_status='Ok')
print(results)


def handle(data, result):
    subject = data['message_title']
    content = data['message'] + '\n' + 'This notification received on: ' + data[
        'created_at'] + '\n' + 'For more information, follow the link: ' + data['url']
    print(content)
    # html_content = render_to_string('mail/email.html', data)
    from_email = ADMIN_USER
    to_send = []
    emails = data['employee_details']
    for key in emails:
        to_send.append(emails[key])

    msg = EmailMessage(subject, content, from_email, to_send)
    # msg.content_subtype = "html"
    # msg.attach_alternative(html_content, "text/html")
    res = msg.send()
    result.sending_status = 'Ok'
    result.save()

    print("Sended")


for result in results:
    data = {'message_title': result.message_title,
            'message': result.message,
            'status': result.status,
            'created_at': str(result.created_at),
            'url': result.url,
            'employee_details': json.loads(result.employee_details.encode())
            }

    handle(data, result)