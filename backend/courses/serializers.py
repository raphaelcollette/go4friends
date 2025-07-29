from rest_framework import serializers
from .models import ClassInfo

class ClassInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassInfo
        fields = ['id', 'descr', 'full_name']