from django.urls import path

from .views import *

# app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', register_view, name='user_registration'),
    path('requisites/', requisites_view, name='user_requisites'),
    path('update/', update_view, name='update'),
    path('delete/', delete_view, name='delete_user'),
    path('requisite-list/', requisite_list_view, name='requisite_list_view'),
    path('requisites_update/<int:pk>/', requisite_update_view, name='requisites_update'),
    path('save_to_result/', save_to_result, name='save_to_result'),
]
