from rest_framework import serializers
from .models import Club, ClubMembership, ClubInvite
from users.serializers import UserPublicSerializer


class ClubSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing club details.
    Includes membership status, privacy, and limited member info.
    """
    is_member = serializers.SerializerMethodField()  # True if request.user is a club member
    members = serializers.SerializerMethodField()    # List of members with role
    is_private = serializers.BooleanField()          # Whether the club is private
    only_member_is_me = serializers.SerializerMethodField()  # True if request.user is the only member
    thread_id = serializers.SerializerMethodField()   # Returns thread ID if available

    class Meta:
        model = Club
        fields = [
            'id', 'name', 'description', 'created_at', 'is_member',
            'members', 'is_private', 'only_member_is_me', 'thread_id'
        ]

    def get_is_member(self, obj):
        """
        Checks if the current request user is a member of the club.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.clubmembership_set.filter(user=request.user).exists()
        return False

    def get_members(self, obj):
        """
        Returns a list of all club members and their roles.
        """
        return [
            {
                "username": membership.user.username,
                "role": membership.role
            }
            for membership in obj.clubmembership_set.all()
        ]

    def get_only_member_is_me(self, obj):
        """
        Returns True if the only club member is the request user.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            members = obj.clubmembership_set.all()
            return members.count() == 1 and members.first().user == request.user
        return False

    def get_thread_id(self, obj):
        """
        Returns the associated thread ID if one exists.
        """
        return obj.thread.id if obj.thread else None


class ClubMembershipSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed club membership entries.
    Includes user info and flag for club ownership.
    """
    user = UserPublicSerializer(read_only=True)  # Nested user serializer
    is_owner = serializers.SerializerMethodField()  # True if user is club owner

    class Meta:
        model = ClubMembership
        fields = ['id', 'user', 'club', 'joined_at', 'is_owner', 'role']

    def get_is_owner(self, obj):
        """
        Determines if the member is the owner of the club.
        """
        return obj.user == obj.club.owner


class ClubCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new clubs.
    Ensures name uniqueness.
    """
    class Meta:
        model = Club
        fields = ['name', 'description', 'is_private']

    def validate_name(self, value):
        """
        Validates that the club name is unique.
        """
        if Club.objects.filter(name=value).exists():
            raise serializers.ValidationError("A club with this name already exists.")
        return value


class ClubInviteSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing club invites.
    Uses string representation for club and inviter.
    """
    club = serializers.StringRelatedField()        # Club name as string
    invited_by = serializers.StringRelatedField()  # Inviter username as string

    class Meta:
        model = ClubInvite
        fields = ['id', 'club', 'invited_by', 'created_at', 'accepted']
