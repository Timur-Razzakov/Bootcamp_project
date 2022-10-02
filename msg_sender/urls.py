from django.urls import path

from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('receive/', receive, name='show'),
    path('subscribe/<int:pk>/', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe, name='unsubscribe'),
    path('my_templates/', ntf_templates_view, name='my_templates'),
    path('template_update/<int:pk>/', template_update_view, name='template_update'),

]
