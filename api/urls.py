from django.urls import path, include
from rest_framework import routers
from .views import (
    LoginView, LogoutView, UserView, KpiGroupViewSet, KpiLevelViewSet,
    KpiViewSet, VariableViewSet
)


router = routers.DefaultRouter()
router.register(r'kpi_group', KpiGroupViewSet, 'kpi_group')
router.register(r'kpi_level', KpiLevelViewSet, 'kpi_level')
router.register(r'kpi', KpiViewSet, 'kpi')
router.register(r'variable', VariableViewSet, 'variable')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserView.as_view(), name='user-detail'),
]