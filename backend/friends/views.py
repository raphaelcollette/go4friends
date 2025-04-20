from rest_framework import generics, permissions, status
from .models import FriendRequest
from .serializers import FriendRequestSerializer
from rest_framework.response import Response

class FriendRequestCreateAPIView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

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
        friend_request_id = request.data.get('friend_request_id')
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, to_user=request.user, status='pending')
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found or already handled.'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.status = 'accepted'
        friend_request.save()
        return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)

class RejectFriendRequestAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        friend_request_id = request.data.get('friend_request_id')
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, to_user=request.user, status='pending')
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found or already handled.'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.status = 'rejected'
        friend_request.save()
        return Response({'message': 'Friend request rejected.'}, status=status.HTTP_200_OK)