from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from .models import FriendRequest
from .serializers import FriendRequestSerializer
from users.serializers import UserPublicSerializer
from rest_framework.permissions import IsAuthenticated
from clubs.models import Club
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes

class SendFriendRequestThrottle(UserRateThrottle):
    rate = '10/hour'

class AcceptFriendRequestThrottle(UserRateThrottle):
    rate = '20/hour'

class RejectFriendRequestThrottle(UserRateThrottle):
    rate = '20/hour'

class CancelFriendRequestThrottle(UserRateThrottle):
    rate = '20/hour'

class RemoveFriendThrottle(UserRateThrottle):
    rate = '10/hour'

class FriendSuggestionsThrottle(UserRateThrottle):
    rate = '30/hour'

class UserFriendsCountThrottle(UserRateThrottle):
    rate = '60/hour'

User = get_user_model()

# --- Friend Requests ---

class FriendRequestCreateAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
   # throttle_classes = [SendFriendRequestThrottle]

    def post(self, request, *args, **kwargs):
        to_username = request.data.get('to_username')
        if not to_username:
            return Response({'error': 'to_username field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(username=to_username)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user, status__in=['pending', 'accepted']).exists():
            return Response({'error': 'Friend request already sent or already friends.'}, status=status.HTTP_400_BAD_REQUEST)

        FriendRequest.objects.create(from_user=request.user, to_user=to_user)

        return Response({'message': 'Friend request sent.'}, status=status.HTTP_201_CREATED)

class FriendRequestListAPIView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')

class AcceptFriendRequestAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [AcceptFriendRequestThrottle]

    def post(self, request, *args, **kwargs):
        return self._handle_friend_request(request, action="accept")

    def _handle_friend_request(self, request, action):
        from_username = request.data.get('from_username')
        if not from_username:
            return Response({'error': 'from_username field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_user = User.objects.get(username=from_username)
            friend_request = FriendRequest.objects.get(from_user=from_user, to_user=request.user, status='pending')
        except (User.DoesNotExist, FriendRequest.DoesNotExist):
            return Response({'error': 'Friend request not found or already handled.'}, status=status.HTTP_404_NOT_FOUND)

        if action == "accept":
            friend_request.status = 'accepted'
            friend_request.save()

            return Response({'message': 'Friend request accepted.'})

        elif action == "reject":
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({'message': 'Friend request rejected.'})

class RejectFriendRequestAPIView(AcceptFriendRequestAPIView):
    #throttle_classes = [RejectFriendRequestThrottle]
    def post(self, request, *args, **kwargs):
        return self._handle_friend_request(request, action="reject")

class CancelFriendRequestAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
   # throttle_classes = [CancelFriendRequestThrottle]

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

class FriendListAPIView(generics.ListAPIView):
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(
            Q(from_user=user) | Q(to_user=user),
            status='accepted'
        )

        friend_users = []
        for friend_request in friends:
            if friend_request.from_user == user:
                friend_users.append(friend_request.to_user)
            else:
                friend_users.append(friend_request.from_user)

        return friend_users

class RemoveFriendAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    #throttle_classes = [RemoveFriendThrottle]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if not username:
            return Response({'error': 'username field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            other_user = User.objects.get(username=username)
            friend_request = FriendRequest.objects.get(
                Q(from_user=request.user, to_user=other_user) |
                Q(from_user=other_user, to_user=request.user),
                status='accepted'
            )
        except (User.DoesNotExist, FriendRequest.DoesNotExist):
            return Response({'error': 'Friend not found.'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.delete()
        return Response({'message': 'Friend removed successfully.'}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@throttle_classes([FriendSuggestionsThrottle])
def friend_suggestions(request):
    me = request.user

    friends = me.friends.all()

    # Only exclude users with PENDING friend requests
    pending_sent = FriendRequest.objects.filter(from_user=me, status='pending').values_list('to_user', flat=True)
    pending_received = FriendRequest.objects.filter(to_user=me, status='pending').values_list('from_user', flat=True)

    excluded_ids = set(friends.values_list('id', flat=True)) | set(pending_sent) | set(pending_received) | {me.id}

    my_club_ids = list(me.clubs.values_list('id', flat=True))
    my_grad_year = me.graduation_year
    my_major = me.major.strip().lower() if me.major else None
    my_interests = set(map(str.lower, me.interests or []))

    candidates = User.objects.exclude(id__in=excluded_ids).prefetch_related('clubs')

    suggestions = []
    for user in candidates:
        reasons = []

        if my_grad_year and user.graduation_year == my_grad_year:
            reasons.append("Same graduation year")

        user_club_ids = {club.id for club in user.clubs.all()}
        if user_club_ids & set(my_club_ids):
            reasons.append("Same club")

        if my_major and user.major:
            user_major = user.major.strip().lower()
            if my_major in user_major or user_major in my_major:
                reasons.append("Similar major")

        user_interests = set(map(str.lower, user.interests or []))
        shared_interests = my_interests & user_interests
        if shared_interests:
            reasons.append(f"Shared interests: {', '.join(sorted(shared_interests))}")

        if reasons:
            data = UserPublicSerializer(user, context={'request': request}).data
            data['match_reasons'] = reasons
            suggestions.append(data)

    return Response(suggestions)

class UserFriendsCountAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
   # throttle_classes = [UserFriendsCountThrottle]

    def get(self, request, username, *args, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        friends = FriendRequest.objects.filter(
            Q(from_user=user) | Q(to_user=user),
            status='accepted'
        )
        count = friends.count()
        return Response({'friends_count': count})