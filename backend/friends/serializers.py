from rest_framework import serializers
from .models import FriendRequest, Notification

class FriendRequestSerializer(serializers.ModelSerializer):
    from_username = serializers.ReadOnlyField(source='from_user.username')
    from_profile_picture = serializers.SerializerMethodField()
    to_username = serializers.ReadOnlyField(source='to_user.username')
    to_profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = [
            'id',
            'from_user', 'from_username', 'from_profile_picture',
            'to_user', 'to_username', 'to_profile_picture',
            'status', 'created_at'
        ]
        read_only_fields = (
            'id',
            'from_user', 'from_username', 'from_profile_picture',
            'to_user', 'to_username', 'to_profile_picture',
            'status', 'created_at'
        )

    def get_from_profile_picture(self, obj):
        user = obj.from_user
        request = self.context.get('request')
        if user.profile_picture and request:
            return request.build_absolute_uri(user.profile_picture.url)
        return None

    def get_to_profile_picture(self, obj):
        user = obj.to_user
        request = self.context.get('request')
        if user.profile_picture and request:
            return request.build_absolute_uri(user.profile_picture.url)
        return None

