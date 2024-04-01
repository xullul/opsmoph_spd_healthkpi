from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]