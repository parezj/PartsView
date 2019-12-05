from django.urls import include, path
from . import views

app_name = "about"

urlpatterns = [
    path('', views.about, name='about'),
]