from django.urls import include, path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = "api"

schema_view = get_schema_view(
   openapi.Info(
      title="PartsView API",
      default_version='v1',
      description="Electronic Parts Search Assistant - Public API",
      contact=openapi.Contact(email="parez.jakub@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('docs', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
    #path('search/(?P<q>\w+)/', views.SearchView.as_view()),
    path('search/<str:q>/', views.SearchView.as_view())
]