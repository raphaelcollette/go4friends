from rest_framework import generics, permissions, status, serializers
from .models import FriendRequest, Notification
from .serializers import FriendRequestSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

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

        existing = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=to_user,
            status__in=['pending', 'accepted']
        )
        if existing.exists():
            return Response({'error': 'Friend request already sent or already friends.'}, status=status.HTTP_400_BAD_REQUEST)

        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        Notification.objects.create(
            user=to_user,
            message=f"{request.user.username} sent you a friend request!"
        )

        return Response({'message': 'Friend request sent.'}, status=status.HTTP_201_CREATED)

class FriendRequestListAPIView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, status='pending')

class FriendListAPIView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(
            (models.Q(from_user=user) | models.Q(to_user=user)),
            status='accepted'
        )

class AcceptFriendRequestAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        from_username = request.data.get('from_username')

        if not from_username:
            return Response({'error': 'from_username field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_user = User.objects.get(username=from_username)
            friend_request = FriendRequest.objects.get(
                from_user=from_user,
                to_user=request.user,
                status='pending'
            )
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
            friend_request = FriendRequest.objects.get(
                from_user=from_user,
                to_user=request.user,
                status='pending'
            )
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
            friend_request = FriendRequest.objects.get(
                from_user=request.user,
                to_user=to_user,
                status='pending'
            )
        except (User.DoesNotExist, FriendRequest.DoesNotExist):
            return Response({'error': 'Friend request not found or cannot be cancelled.'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.delete()
        return Response({'message': 'Friend request cancelled.'}, status=status.HTTP_200_OK)

class NotificationListAPIView(generics.ListAPIView):
    serializer_class = serializers.Serializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        data = [
            {
                "id": n.id,
                "message": n.message,
                "is_read": n.is_read,
                "created_at": n.created_at
            } for n in notifications
        ]
        return Response(data, status=status.HTTP_200_OK)

