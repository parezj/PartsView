from django.urls import include, path
from . import views

app_name = "ajax"

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('query/', views.query, name='query'),
    path('fav-add/', views.fav_add, name='fav_add'),
    path('fav-del/', views.fav_del, name='fav_del'),
    path('fav-flush/', views.fav_flush, name='fav_flush'),
    path('hist-flush/', views.hist_flush, name='hist_flush'),
]