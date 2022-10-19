import os
import sys

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "natification_service.settings")
import django

django.setup()
# -----------------------------------------------------------------------------------------------
import pika
import json
from msg_sender.models import Notification_group, Notification

""" Получаем данные из внешнего сервиса (RabbitMQ) и сохраняем в бд"""
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
    channel = connection.channel()

    channel.queue_declare(queue='notification', durable=True)

    # получаем данные и сохраняем их в модельку
    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
        ntf_group = Notification_group.objects.get(id=data["notification_group"])
        ntf = Notification.objects.create()
        ntf.title = data["title"]
        ntf.status = data["status"]
        ntf.url = data["url"]
        ntf.message = data["message"]
        ntf.created_at = data["created_at"]
        ntf.ntf_group = ntf_group
        ntf.recipient = data["recipient"]
        ntf.save()

    channel.basic_consume(queue='notification', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
