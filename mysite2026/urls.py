"""
URL configuration for mysite2026 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse

def info(request):
    ip_addres = request.META['REMOTE_ADDR']
    res = f"<h1>you Ip address is : {ip_addres}</h1>"
    for name, value in request.META.items():
        res += f"<p>{name}: {value}</p>"
    return HttpResponse(res)

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')


urlpatterns = [
    path('', index),
    path('home/', home),
    path('info/', info),
    path('admin/', admin.site.urls),
]
