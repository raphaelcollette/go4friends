from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Thread, ThreadParticipant, Message
from .serializers import MessageSerializer, ThreadSerializer
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

User = get_user_model()

class ThreadListAPIView(generics.ListAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Thread.objects.filter(participants__user=self.request.user).distinct()


class ThreadDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        thread_id = self.kwargs.get('pk')
        thread = get_object_or_404(Thread, id=thread_id, participants__user=self.request.user)
        return thread


class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        thread_id = self.kwargs.get('thread_id')
        return Message.objects.filter(
            thread_id=thread_id,
            thread__participants__user=self.request.user
        )


@method_decorator(ratelimit(key='user', rate='10/m', block=True), name='dispatch')
class SendMessageAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        thread_id = kwargs.get('thread_id')
        thread = get_object_or_404(Thread, id=thread_id, participants__user=request.user)
        message = request.data.get('message')

        if not message:
            return Response({'error': 'Message cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        msg = Message.objects.create(
            thread=thread,
            sender=request.user,
            message=message
        )

        return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)


class StartPrivateThreadAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({'error': 'Username required.'}, status=400)

        try:
            other_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        # Look for existing private thread
        threads = Thread.objects.filter(
            is_group=False,
            participants__user=request.user
        ).filter(
            participants__user=other_user
        ).distinct()

        if threads.exists():
            thread = threads.first()
        else:
            thread = Thread.objects.create(is_group=False)
            ThreadParticipant.objects.create(thread=thread, user=request.user)
            ThreadParticipant.objects.create(thread=thread, user=other_user)

        return Response({'thread_id': thread.id})