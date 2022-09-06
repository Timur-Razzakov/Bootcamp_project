from django.urls import path
from .views import *
# app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', register_view, name='user_registration'),
    path('requisites/', requisites_view, name='user_requisites'),
    # path('delete/', delete_view, name='delete_user'),
    # path('contact/', contact_view, name='contact'),
]