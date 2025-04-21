from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import models

from .models import FriendRequest, Notification
from .serializers import FriendRequestSerializer, NotificationSerializer
from users.serializers import UserPublicSerializer  # optional if needed later

User = get_user_model()

# --- Friend Requests ---

class FriendRequestCreateAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        to_username = request.data.get('to_username')

        if not to_username:
            return Response({'error': 'to_username field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(username=to_username)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if FriendRequest.objects.filter(
            from_user=request.user,
            to_user=to_user,
            status__in=['pending', 'accepted']
        ).exists():
            return Response({'error': 'Friend request already sent or already friends.'}, status=status.HTTP_400_BAD_REQUEST)

        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        Notification.objects.create(user=to_user, message=f"{request.user.username} sent you a friend request!")

        return Response({'message': 'Friend request sent.'}, status=status.HTTP_201_CREATED)

class FriendRequestListAPIView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')

class AcceptFriendRequestAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        from_username = request.data.get('from_username')

        if not from_username:
            return Response({'error': 'from_username field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_user = User.objects.get(username=from_username)
            friend_request = FriendRequest.objects.get(from_user=from_user, to_user=request.user, status='pending')
        except (User.DoesNotExist, FriendRequest.DoesNotExist):
            return Response({'error': 'Friend request not found or already handled.'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.status = 'accepted'
        friend_request.save()

        return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)

class RejectFriendRequestAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        from_username = request.data.get('from_username')

        if not from_username:
            return Response({'error': 'from_username field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_user = User.objects.get(username=from_username)
            friend_request = FriendRequest.objects.get(from_user=from_user, to_user=request.user, status='pending')
        except (User.DoesNotExist, FriendRequest.DoesNotExist):
            return Response({'error': 'Friend request not found or already handled.'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.status = 'rejected'
        friend_request.save()

        return Response({'message': 'Friend request rejected.'}, status=status.HTTP_200_OK)

class CancelFriendRequestAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        to_username = request.data.get('to_username')

        if not to_username:
            return Response({'error': 'to_username field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(username=to_username)
            friend_request = FriendRequest.objects.get(from_user=request.user, to_user=to_user, status='pending')
        except (User.DoesNotExist, FriendRequest.DoesNotExist):
            return Response({'error': 'Friend request not found or cannot be cancelled.'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.delete()
        return Response({'message': 'Friend request cancelled.'}, status=status.HTTP_200_OK)

# --- Friend List (accepted friends) ---

class FriendListAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        friends = FriendRequest.objects.filter(
            (models.Q(from_user=user) | models.Q(to_user=user)),
            status='accepted'
        )

        friend_users = []
        for friend_request in friends:
            if friend_request.from_user == user:
                friend_users.append(friend_request.to_user)
            else:
                friend_users.append(friend_request.from_user)

        serializer = UserPublicSerializer(friend_users, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class RemoveFriendAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')

        if not username:
            return Response({'error': 'username field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            other_user = User.objects.get(username=username)
            friend_request = FriendRequest.objects.get(
                (models.Q(from_user=request.user, to_user=other_user) | models.Q(from_user=other_user, to_user=request.user)),
                status='accepted'
            )
        except (User.DoesNotExist, FriendRequest.DoesNotExist):
            return Response({'error': 'Friend not found.'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.delete()
        return Response({'message': 'Friend removed successfully.'}, status=status.HTTP_200_OK)

# --- Notifications ---

class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class MarkNotificationsReadAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message': 'All notifications marked as read.'}, status=status.HTTP_200_OK)

class ClearNotificationsAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Notification.objects.filter(user=request.user).delete()
        return Response({'message': 'All notifications cleared.'}, status=status.HTTP_200_OK)

