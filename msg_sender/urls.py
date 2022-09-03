from django.urls import path

from .views import *
urlpatterns = [
    path('', home_view, name='home'),
    path('receive/',receive, name = 'show')

]
