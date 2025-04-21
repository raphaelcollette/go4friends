from rest_framework import serializers
from .models import User

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'bio', 'location', 'profile_picture']