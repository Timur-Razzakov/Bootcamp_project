import os, sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "natification_service.settings")
import django

django.setup()
# -------------------------------------------------------------------------------
admins = [
    99169335
]

db_name = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')

POSTGRES_URI = f'postgresql//{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{db_name}'
