from rest_framework import serializers
from .models import Club, ClubMembership
from users.serializers import UserPublicSerializer


class ClubSerializer(serializers.ModelSerializer):
    is_member = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'created_at', 'is_member', 'members']

    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.clubmembership_set.filter(user=request.user).exists()
        return False

    def get_members(self, obj):
        return [
            {
                "username": membership.user.username,
                "role": membership.role
            }
            for membership in obj.clubmembership_set.all()
        ]

class ClubMembershipSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = ClubMembership
        fields = ['id', 'user', 'club', 'joined_at', 'is_owner', 'role']

    def get_is_owner(self, obj):
        return obj.user == obj.club.owner
    
    