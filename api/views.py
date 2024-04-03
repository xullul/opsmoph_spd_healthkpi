from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.request import HttpRequest, Request
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


class LoginView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    
    def post(self, request: HttpRequest) -> Response:
        username: str | None = request.POST.get('username')
        password: str | None = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user, password)
            return Response({'message': 'Login successful'}, status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status.HTTP_401_UNAUTHORIZED)
        

class LogoutView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request: HttpRequest) -> Response:
        logout(request)
        return Response({'message': 'Logout successful'}, status.HTTP_200_OK)


class UserView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
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
    permission_classes = [AllowAny]


class KpiLevelViewSet(viewsets.ModelViewSet):
    queryset = KpiLevel.objects.all().order_by('pk')
    serializer_class = KpiLevelSerializer
    permission_classes = [AllowAny]


class KpiViewSet(viewsets.ModelViewSet):
    queryset = Kpi.objects.all()
    serializer_class = KpiSerializer
    permission_classes = [AllowAny]


class VariableViewSet(viewsets.ModelViewSet):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer
    permission_classes = [AllowAny]


class AboutView(APIView):
    def get(self, request, format=None):
        data = {
            
        }
        return Response()