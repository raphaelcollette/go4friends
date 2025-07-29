from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Thread, ThreadParticipant, Message

User = get_user_model()


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'profile_picture']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSummarySerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'message', 'timestamp', 'is_read', 'pinned']


class ThreadParticipantSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = ThreadParticipant
        fields = ['user', 'joined_at']


class ThreadSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    club_name = serializers.SerializerMethodField() 
    class_info = ClassInfoSerializer(read_only=True)
    is_group = serializers.BooleanField(read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'name', 'is_group', 'participants', 'last_message', 'created_at', 'club_name', 'class_info']

    def get_participants(self, obj):
        participants = ThreadParticipant.objects.filter(thread=obj).select_related('user')
        return ThreadParticipantSerializer(participants, many=True).data

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-timestamp').first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def get_club_name(self, obj):
        if hasattr(obj, 'club') and obj.club:
            return obj.club.name
        return None