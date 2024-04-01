from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from healthkpi.models import KpiGroup, KpiLevel, Kpi, Variable
from .serializers import (
    UserSerializer,
    KpiGroupSerializer,
    KpiLevelSerializer,
    KpiSerializer,
    VariableSerializer
)
from .paginations import (
    SmallPageNumberPagination,
    MediumPageNumberPagination,
    LargePageNumberPagination
)


class UserView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MediumPageNumberPagination
    
    def list(self, request: Request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def detail(self, instance: User, request: Request):
        serializer = UserSerializer(instance)
        return Response(serializer.data)
        
    def create(self, request: Request):
        serializer = UserSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        else:
            return Response(serializer.data, 400)


class KpiGroupViewSet(viewsets.ModelViewSet):
    queryset = KpiGroup.objects.all().order_by('pk')
    serializer_class = KpiGroupSerializer
    permission_classes = [permissions.AllowAny]


class KpiLevelViewSet(viewsets.ModelViewSet):
    queryset = KpiLevel.objects.all().order_by('pk')
    serializer_class = KpiLevelSerializer
    permission_classes = [permissions.AllowAny]


class KpiViewSet(viewsets.ModelViewSet):
    queryset = Kpi.objects.all()
    serializer_class = KpiSerializer
    permission_classes = [permissions.AllowAny]


class VariableViewSet(viewsets.ModelViewSet):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer
    permission_classes = [permissions.AllowAny]


class AboutView(APIView):
    def get(self, request, format=None):
        data = {
            
        }
        return Response()