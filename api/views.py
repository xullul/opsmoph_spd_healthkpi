from rest_framework import viewsets
from rest_framework import permissions
from healthkpi.models import (
    KpiGroup, KpiLevel
)
from .serializers import (
    KpiGroupSerializer,
    KpiLevelSerializer
)


class KpiGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KpiGroup.objects.all().order_by('pk')
    serializer_class = KpiGroupSerializer
    permission_classes = [permissions.AllowAny]


class KpiLevelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KpiLevel.objects.all().order_by('pk')
    serializer_class = KpiLevelSerializer
    permission_classes = [permissions.AllowAny]