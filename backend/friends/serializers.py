from rest_framework import serializers
from .models import FriendRequest

class FriendRequestSerializer(serializers.ModelSerializer):
    from_username = serializers.ReadOnlyField(source='from_user.username')
    from_profile_picture = serializers.ImageField(source='from_user.profile_picture', read_only=True)  # ADD THIS
    to_username = serializers.ReadOnlyField(source='to_user.username')

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'from_username', 'from_profile_picture', 'to_user', 'to_username', 'status', 'created_at']
        read_only_fields = ['from_user', 'from_username', 'from_profile_picture', 'to_username', 'created_at']