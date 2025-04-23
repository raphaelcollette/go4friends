from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Message
from .serializers import MessageSerializer
from django.db import models

User = get_user_model()

class SendMessageAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        receiver_username = request.data.get('receiver')
        message = request.data.get('message')

        if not receiver_username or not message:
            return Response({'error': 'Receiver and message are required.'}, status=400)

        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response({'error': 'Receiver not found.'}, status=404)

        msg = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            message=message
        )

        return Response(MessageSerializer(msg).data, status=201)

class ThreadAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.request.query_params.get('with')
        other_user = User.objects.get(username=username)
        return Message.objects.filter(
            models.Q(sender=self.request.user, receiver=other_user) |
            models.Q(sender=other_user, receiver=self.request.user)
        )
