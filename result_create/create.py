import schedule
from jinja2 import Template
import os, sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "natification_service.settings")
import django

django.setup()

from accounts.models import Result, Empl_requisites
from msg_sender.models import Notification, Channel, NTF_type_for_channel


def handle():
    notifications = Notification.objects.filter(processing_status=False)
    for notification in notifications:
        ntf_group = notification.ntf_group
        channel_names = Channel.objects.all()
        for channel_name in channel_names:  # tg
            res_for_send = Result.objects.create()
            res_for_send.channels = channel_name
            res_for_send.notification = notification
            all_requisites = Empl_requisites.objects.filter(channel=channel_name)
            for requisite in all_requisites:
                res_for_send.employee_details.add(requisite)
            templates = NTF_type_for_channel.objects.get(channel=channel_name,
                                                        ntf_group=ntf_group)
            tm_message = Template(templates.templates_for_massage)
            msg = tm_message.render(message_title=notification.title,
                                    status=notification.status,
                                    message=notification.message,
                                    created_at=notification.created_at,
                                    url=notification.url)
            res_for_send.message = msg
            res_for_send.created_at = notification.created_at
            res_for_send.save()
            notification.processing_status = True
            notification.save()
            print("Данные сохранены")



def main():
    # Это планировшик, он каждый n секунд(seconds)/минут(minutes) сможет запускать код
    schedule.every(5).seconds.do(handle)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()