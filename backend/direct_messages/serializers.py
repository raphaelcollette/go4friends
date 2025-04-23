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
        fields = ['id', 'sender', 'message', 'timestamp', 'is_read']


class ThreadParticipantSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = ThreadParticipant
        fields = ['user', 'joined_at']


class ThreadSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    is_group = serializers.BooleanField(read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'name', 'is_group', 'participants', 'last_message', 'created_at']

    def get_participants(self, obj):
        participants = ThreadParticipant.objects.filter(thread=obj).select_related('user')
        return ThreadParticipantSerializer(participants, many=True).data

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-timestamp').first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None