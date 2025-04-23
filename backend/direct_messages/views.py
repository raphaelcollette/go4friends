from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Thread, ThreadParticipant, Message
from .serializers import MessageSerializer, ThreadSerializer
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.db.models import Count

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
        usernames = request.data.get('usernames', [])

        if not isinstance(usernames, list):
            return Response({'error': 'Usernames must be a list.'}, status=status.HTTP_400_BAD_REQUEST)

        # Add current user if not included
        if request.user.username not in usernames:
            usernames.append(request.user.username)

        # Get unique usernames
        usernames = list(set(usernames))

        if len(usernames) < 2:
            return Response({'error': 'At least two users are required to start a thread.'}, status=400)

        # Get user objects
        users = list(User.objects.filter(username__in=usernames))
        if len(users) != len(usernames):
            return Response({'error': 'One or more users not found.'}, status=404)

        # Try to find an existing thread with the exact same users
        possible_threads = Thread.objects.annotate(num_participants=Count('participants')).filter(
            num_participants=len(users),
            is_group=(len(users) > 2)
        )

        for thread in possible_threads:
            thread_usernames = list(thread.participants.values_list('user__username', flat=True))
            if sorted(thread_usernames) == sorted(usernames):
                return Response({'thread_id': thread.id})

        # No existing thread, create one
        thread = Thread.objects.create(is_group=(len(users) > 2))
        for user in users:
            ThreadParticipant.objects.create(thread=thread, user=user)

        return Response({'thread_id': thread.id})