from django.urls import include, path
from . import views

app_name = "history"

urlpatterns = [
    path('', views.history, name='history'),
]