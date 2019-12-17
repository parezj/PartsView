from django.urls import include, path
from . import views

app_name = "part"

urlpatterns = [
    path('', views.part, name='part'),
]