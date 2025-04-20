from rest_framework import serializers
from .models import FriendRequest

class FriendRequestSerializer(serializers.ModelSerializer):
    from_username = serializers.ReadOnlyField(source='from_user.username')
    to_username = serializers.ReadOnlyField(source='to_user.username')

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'from_username', 'to_user', 'to_username', 'status', 'created_at']
        read_only_fields = ['from_user', 'from_username', 'to_username', 'created_at']
