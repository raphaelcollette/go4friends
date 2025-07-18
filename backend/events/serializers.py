from rest_framework import serializers
from .models import Event
from better_profanity import profanity


profanity.load_censor_words()

class EventSerializer(serializers.ModelSerializer):
    club = serializers.SerializerMethodField()
    is_going = serializers.SerializerMethodField()
    attendee_count = serializers.SerializerMethodField()
    image = serializers.URLField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date',
            'club', 'image', 'location', 'is_going', 'attendee_count'
        ]

    def get_club(self, obj):
        return obj.club.name if obj.club else None

    def get_is_going(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.attendees.filter(id=request.user.id).exists()
        return False

    def get_attendee_count(self, obj):
        return obj.attendees.count()

    def validate_title(self, value):
        if profanity.contains_profanity(value):
            raise serializers.ValidationError("Event title contains inappropriate language.")
        return value

    def validate_description(self, value):
        if profanity.contains_profanity(value):
            raise serializers.ValidationError("Event description contains inappropriate language.")
        return value