from django.urls import path
from . import views

app_name = 'chopee'

urlpatterns = [
    path('', views.index, name='index'),
]
