from django.urls import path

from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('receive/', receive, name='show'),

    path('save_to_result/', save_to_result, name='save_to_result'),
    path('add_ntf_templates/', ntf_templates_view, name='add_ntf_templates')


]
