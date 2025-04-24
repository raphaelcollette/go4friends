from rest_framework import serializers
from .models import Club, ClubMembership, ClubInvite
from users.serializers import UserPublicSerializer


class ClubSerializer(serializers.ModelSerializer):
    is_member = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    is_private = serializers.BooleanField()
    only_member_is_me = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'created_at', 'is_member', 'members', 'is_private', 'only_member_is_me']

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

    def get_only_member_is_me(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            members = obj.clubmembership_set.all()
            return members.count() == 1 and members.first().user == request.user
        return False

class ClubMembershipSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = ClubMembership
        fields = ['id', 'user', 'club', 'joined_at', 'is_owner', 'role']

    def get_is_owner(self, obj):
        return obj.user == obj.club.owner
        
class ClubCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['name', 'description', 'is_private']

    def validate_name(self, value):
        if Club.objects.filter(name=value).exists():
            raise serializers.ValidationError("A club with this name already exists.")
        return value

class ClubInviteSerializer(serializers.ModelSerializer):
    club = serializers.StringRelatedField()
    invited_by = serializers.StringRelatedField()

    class Meta:
        model = ClubInvite
        fields = ['id', 'club', 'invited_by', 'created_at', 'accepted']
    