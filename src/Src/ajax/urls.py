from django.urls import include, path
from . import views

app_name = "ajax"

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('query/', views.query, name='query'),
]