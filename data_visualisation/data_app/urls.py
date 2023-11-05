from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='data_app_index'),
    path('upload/', views.upload, name='data_app_upload'),
    path('result/', views.result, name='data_app_result')     
]