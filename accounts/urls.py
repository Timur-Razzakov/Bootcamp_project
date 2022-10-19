from django.urls import path

from .views import *

# app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login'),# тестим
    path('logout/', logout_view, name='logout'),
    path('registration/', register_view, name='user_registration'),# тестим
    path('requisites/', requisites_view, name='user_requisites'),# тестим
    path('update/', update_view, name='update'),# тестим
    path('delete/', delete_view, name='delete_user'),
    path('requisite_list/', requisite_list_view, name='requisite_list'),# тестим
    path('requisites_update/<str:pk>/', requisite_update_view, name='requisites_update'),# тестим
]
