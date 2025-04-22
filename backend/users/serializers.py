from rest_framework import serializers
from django.contrib.auth import get_user_model
from friends.models import FriendRequest
from django.db.models import Q

User = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    clubs = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()
    friend_request_sent = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
            'bio',
            'location',
            'profile_picture',
            'clubs',
            'is_friend',
            'friend_request_sent',
            'interests',
        ]
        read_only_fields = fields

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None

    def get_clubs(self, obj):
        return [{'id': club.id, 'name': club.name} for club in obj.clubs.all()]

    def get_is_friend(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        if obj == request.user:
            return False  # You can't be "friends" with yourself
        
        return FriendRequest.objects.filter(
            (Q(from_user=request.user, to_user=obj) | Q(from_user=obj, to_user=request.user)),
            status='accepted'
        ).exists()

    def get_friend_request_sent(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        if obj == request.user:
            return False

        return FriendRequest.objects.filter(
            from_user=request.user, to_user=obj,
            status='pending'
        ).exists()