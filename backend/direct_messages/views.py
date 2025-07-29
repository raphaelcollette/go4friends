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
from rest_framework.views import APIView
from friends.models import FriendRequest 
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from courses.models import ClassInfo

User = get_user_model()

class SendMessageThrottle(UserRateThrottle):
    rate = '20/min'

class StartThreadThrottle(UserRateThrottle):
    rate = '10/min'

class TogglePinThrottle(UserRateThrottle):
    rate = '30/min'

def are_friends(user1, user2):
    """Helper function to check if two users are friends"""
    return FriendRequest.objects.filter(
        Q(from_user=user1, to_user=user2) | Q(from_user=user2, to_user=user1),
        status='accepted'
    ).exists()

class ThreadListAPIView(generics.ListAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Thread.objects.filter(participants__user=self.request.user).select_related('club').distinct()


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


class SendMessageAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    #throttle_classes = [SendMessageThrottle]

    def post(self, request, *args, **kwargs):
        thread_id = kwargs.get('thread_id')
        thread = get_object_or_404(Thread, id=thread_id, participants__user=request.user)
        
        # Check if user is friends with all other participants in the thread
        other_participants = thread.participants.exclude(user=request.user)
        for participant in other_participants:
            if not are_friends(request.user, participant.user):
                return Response({
                    'error': f'You can only send messages to friends. You are not friends with {participant.user.username}.'
                }, status=status.HTTP_403_FORBIDDEN)
        
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
    #throttle_classes = [StartThreadThrottle]

    def post(self, request):
        usernames = request.data.get('usernames') or []
        
        # Handle legacy 'username' key for private 1-1 chat
        single_username = request.data.get('username')
        if single_username:
            usernames = [single_username]

        if not usernames:
            return Response({'error': 'Username(s) required.'}, status=400)

        users = list(User.objects.filter(username__in=usernames).distinct())
        if len(users) != len(usernames):
            return Response({'error': 'One or more users not found.'}, status=404)

        # CHECK FRIENDSHIP FOR ALL USERS
        for user in users:
            if not are_friends(request.user, user):
                return Response({
                    'error': f'You can only start conversations with friends. You are not friends with {user.username}.'
                }, status=status.HTTP_403_FORBIDDEN)

        # Private 1-1 chat
        if len(users) == 1:
            other_user = users[0]
            existing = Thread.objects.filter(
                is_group=False,
                participants__user=request.user
            ).filter(participants__user=other_user).distinct()
            if existing.exists():
                return Response({'thread_id': existing.first().id})
            thread = Thread.objects.create(is_group=False)
            ThreadParticipant.objects.bulk_create([
                ThreadParticipant(thread=thread, user=request.user),
                ThreadParticipant(thread=thread, user=other_user)
            ])
            return Response({'thread_id': thread.id})

        # Group chat
        thread = Thread.objects.create(is_group=True)
        ThreadParticipant.objects.create(thread=thread, user=request.user)
        for user in users:
            if user != request.user:
                ThreadParticipant.objects.create(thread=thread, user=user)
        return Response({'thread_id': thread.id})

class TogglePinMessageAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
   # throttle_classes = [TogglePinThrottle]

    def post(self, request, pk):
        message = get_object_or_404(Message, id=pk, thread__participants__user=request.user)
        message.pinned = not message.pinned
        message.save()
        return Response({'status': 'pinned' if message.pinned else 'unpinned'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_or_create_class_thread(request):
    class_id = request.data.get('class_id')
    if not class_id:
        return Response({'error': 'class_id is required'}, status=400)

    class_obj = get_object_or_404(ClassInfo, id=class_id)

    thread = Thread.objects.filter(class_info=class_obj).first()
    if not thread:
        thread = Thread.objects.create(class_info=class_obj, name=class_obj.full_name, is_group=True)
        ThreadParticipant.objects.create(thread=thread, user=request.user)
    else:
        # If thread exists, ensure user is participant
        if not ThreadParticipant.objects.filter(thread=thread, user=request.user).exists():
            ThreadParticipant.objects.create(thread=thread, user=request.user)

    serializer = ThreadSerializer(thread, context={'request': request})
    return Response(serializer.data)