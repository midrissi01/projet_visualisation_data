from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='data_app_index'),
   
      
]