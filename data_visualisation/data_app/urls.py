from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='data_app_index'),
    path('barplot/upload', views.barplot_upload, name='barplot_upload'),
    path('barplot/result',views.barplot_result, name='barplot_result'),
    path('lineplot/upload', views.lineplot_upload, name='lineplot_upload'),
    path('lineplot/result', views.lineplot_result, name='lineplot_result'),
    path('scatterplot/upload', views.scatterplot_upload, name='scatterplot_upload'),
    path('scatterplot/result', views.scatterplot_result, name='scatterplot_result'),
    
    path('piechart/upload', views.piechart_upload, name='piechart_upload'),
    path('piechart/result', views.piechart_result, name='piechart_result'),
    


    
]