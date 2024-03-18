from rest_framework import serializers
from healthkpi.models import (
    KpiGroup, KpiLevel
)


class KpiGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = KpiGroup
        fields = '__all__'


class KpiLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = KpiLevel
        fields = '__all__'