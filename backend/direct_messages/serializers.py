from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp', 'is_read']

    def get_sender(self, obj):
        return obj.sender.username