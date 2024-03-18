from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'kpi_group', views.KpiGroupViewSet.as_view(), 'kpi_group')
router.register(r'kpi_level', views.KpiLevelViewSet.as_view(), 'kpi_level')

urlpatterns = [
    path('', include(router.urls)),
]