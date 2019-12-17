from django.urls import include, path
from . import views

app_name = "basic"

urlpatterns = [
    path('', views.home, name='home'),
]
