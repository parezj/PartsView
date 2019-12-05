from django.urls import include, path
from . import views

app_name = "api"

urlpatterns = [
    path('', views.api, name='api'),
]