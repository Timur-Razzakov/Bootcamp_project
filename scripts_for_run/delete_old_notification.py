import os
import sys

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "natification_service.settings")
import django

django.setup()
# ---------------------------------------------------------------------------------

import time
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from schedule import every, repeat, run_pending

from msg_sender.models import Notification
from accounts.models import Result

"""
Функция для удаления старых записей
"""


class Command(BaseCommand):
    help = 'Delete objects older than 5 days'

    @repeat(every().sunday.at("15:25"))
    def handle(*args, **options):
        Notification.objects.filter(created_at__lte=datetime.now() - timedelta(days=5)).delete()
        Result.objects.filter(created_at__lte=datetime.now() - timedelta(days=5)).delete()


while 1:
    run_pending()
    time.sleep(1)
