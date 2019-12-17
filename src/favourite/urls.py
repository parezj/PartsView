from django.urls import include, path
from . import views

app_name = "favourite"

urlpatterns = [
    path('', views.favourite, name='favourite'),
]