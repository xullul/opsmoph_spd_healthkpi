from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from healthkpi.models import (
    KpiGroup, KpiLevel, Kpi, Variable
)
from typing import Any, Dict


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data: Dict[str, Any]) -> User:
        return User.objects.create(**validated_data)

    def update(self, instance: User, validated_data: Dict[str, Any]) -> User:
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class KpiGroupSerializer(ModelSerializer):
    class Meta:
        model = KpiGroup
        fields = '__all__'


class KpiLevelSerializer(ModelSerializer):
    class Meta:
        model = KpiLevel
        fields = '__all__'


class KpiSerializer(ModelSerializer):
    class Meta:
        model = Kpi
        fields = '__all__'


class VariableSerializer(ModelSerializer):
    class Meta:
        model = Variable
        fields = '__all__'