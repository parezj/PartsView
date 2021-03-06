"""parts_view URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (
handler400, handler403, handler404, handler500
 )
 
from basic import views as basic_views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import debug_toolbar

from django.views.generic.base import RedirectView


favicon_view = RedirectView.as_view(url='/static/favicon/favicon.ico', permanent=True)
favicon_view = RedirectView.as_view(url='/static/js/fa.js', permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('login/', basic_views.login, name='login'),
    path('register/', basic_views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='logout'),
    
    path('about/', include('about.urls')),
    path('api/', include('api.urls')),
    path('history/', include('history.urls')),
    path('favourite/', include('favourite.urls')),
    path('part/<str:searched>/<str:part>', include('part.urls')),
    path('search/<str:part>', include('search.urls')),
    path('ajax/', include('ajax.urls')),
    
    path('', include('basic.urls')),

    path('__debug__/', include(debug_toolbar.urls)),
    
    re_path(r'^favicon\.ico$', favicon_view),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = 'basic.views.handler404'