from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
import os

def info(request):
    data =  {}
    print(request.META)
    for k,v in request.META.items():
        data[k] = v
        print(k, "=", v)
    return JsonResponse(data)

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')

def shopping(request):
    return render(request, 'shopping.html')

def pdf_view(request):
    filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '00046f2020061915224768.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
