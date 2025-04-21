from rest_framework import serializers
from .models import Club, ClubMembership

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'owner', 'created_at']

class ClubMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubMembership
        fields = ['id', 'user', 'club', 'joined_at']