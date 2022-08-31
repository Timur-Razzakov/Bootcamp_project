from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.


def home_view(request):
    return render(request, 'home.html', {})