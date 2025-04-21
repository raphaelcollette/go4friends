from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    club = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'club', 'image']

    def get_club(self, obj):
        return obj.club.name if obj.club else None