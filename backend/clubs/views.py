from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Club, ClubMembership, ClubInvite
from .serializers import ClubSerializer, ClubMembershipSerializer, ClubCreateSerializer, ClubInviteSerializer
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from direct_messages.models import Thread, ThreadParticipant
from .utils import add_user_to_club_chat

User = get_user_model()


class ClubCreateAPIView(generics.GenericAPIView):
    serializer_class = ClubCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 1. Create chat thread
            thread = Thread.objects.create(is_group=True)

            # 2. Save club and link thread
            club = serializer.save(owner=request.user, thread=thread)

            # 3. Add creator to club and chat
            ClubMembership.objects.create(user=request.user, club=club, role='admin')
            ThreadParticipant.objects.create(thread=thread, user=request.user)

            # 4. Return serialized data
            return Response(ClubSerializer(club, context={'request': request}).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClubListAPIView(generics.ListAPIView):
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticated] 
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        queryset = Club.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset

    def get_serializer_context(self):
        # Pass the request to the serializer so it can check is_member
        return {'request': self.request}


class ClubJoinAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, club_name, *args, **kwargs):
        club = get_object_or_404(Club, name=club_name)

        # 🔐 Private club? Require accepted invite
        if club.is_private:
            invite_exists = ClubInvite.objects.filter(club=club, invitee=request.user, accepted=True).exists()
            if not invite_exists:
                return Response(
                    {'error': 'This club is private and requires an accepted invite to join.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        # ✅ Safe creation — no IntegrityError even if already joined
        membership, created = ClubMembership.objects.get_or_create(
            user=request.user,
            club=club,
            defaults={'role': 'member'}
        )

        # ✅ Add to chat if new or if not already added
        add_user_to_club_chat(club, request.user)

        return Response(
            {'message': f'Joined {club.name} successfully!' if created else 'Already a member.'},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class ClubLeaveAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, club_name, *args, **kwargs):
        try:
            club = Club.objects.get(name=club_name)
        except Club.DoesNotExist:
            return Response({'error': 'Club not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            membership = ClubMembership.objects.get(user=request.user, club=club)
            membership.delete()

            # ✅ Remove from club chat if thread exists
            if club.thread:
                ThreadParticipant.objects.filter(thread=club.thread, user=request.user).delete()

            # ✅ Clean up any invite (so user can be invited again later)
            ClubInvite.objects.filter(club=club, invitee=request.user).delete()

            return Response({'message': f'Left {club.name} successfully.'}, status=status.HTTP_200_OK)
        except ClubMembership.DoesNotExist:
            return Response({'error': 'You are not a member of this club.'}, status=status.HTTP_400_BAD_REQUEST)


class ClubDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, club_name):
        try:
            club = Club.objects.get(name=club_name)
        except Club.DoesNotExist:
            return Response({'error': 'Club not found.'}, status=status.HTTP_404_NOT_FOUND)

        members = ClubMembership.objects.filter(club=club)
        member_data = ClubMembershipSerializer(members, many=True, context={'request': request}).data
        
        return Response({
            'club': ClubSerializer(club, context={'request': request}).data,
            'members': member_data
        })

class IsClubAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        club_name = request.data.get('club_name')
        if not club_name:
            return False  # not a club event or malformed

        try:
            membership = ClubMembership.objects.get(user=request.user, club__name=club_name)
            return membership.role == 'admin'
        except ClubMembership.DoesNotExist:
            return False

class ClubDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, club_name, *args, **kwargs):
        try:
            club = Club.objects.get(name=club_name)
        except Club.DoesNotExist:
            return Response({'error': 'Club not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            membership = ClubMembership.objects.get(user=request.user, club=club)
        except ClubMembership.DoesNotExist:
            return Response({'error': 'You are not a member of this club.'}, status=status.HTTP_403_FORBIDDEN)

        if membership.role != 'admin':
            return Response({'error': 'Only club admins can delete the club.'}, status=status.HTTP_403_FORBIDDEN)

        # ✅ Delete the linked chat thread if it exists
        if club.thread:
            club.thread.delete()

        club.delete()
        return Response({'message': 'Club deleted successfully.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_member_role(request, club_name):
    club = get_object_or_404(Club, name=club_name)
    membership = club.clubmembership_set.filter(user=request.user).first()

    if not membership or membership.role != 'admin':
        return Response({'error': 'Only admins can update roles.'}, status=status.HTTP_403_FORBIDDEN)

    username = request.data.get('username')
    new_role = request.data.get('role')

    if new_role not in ['admin', 'moderator', 'member']:
        return Response({'error': 'Invalid role.'}, status=status.HTTP_400_BAD_REQUEST)

    target_user = get_object_or_404(User, username=username)
    target_membership = club.clubmembership_set.filter(user=target_user).first()

    if not target_membership:
        return Response({'error': 'User is not a member of the club.'}, status=status.HTTP_404_NOT_FOUND)

    target_membership.role = new_role
    target_membership.save()

    return Response({'message': f"{username}'s role updated to {new_role}."})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_member(request, club_name):
    username = request.data.get('username')
    if not username:
        return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        club = Club.objects.get(name=club_name)
    except Club.DoesNotExist:
        return Response({'error': 'Club not found.'}, status=status.HTTP_404_NOT_FOUND)

    requester_membership = club.clubmembership_set.filter(user=request.user).first()
    target_membership = club.clubmembership_set.filter(user__username=username).first()

    if not requester_membership or not target_membership:
        return Response({'error': 'Membership not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Prevent users from removing themselves
    if request.user.username == username:
        return Response({'error': 'You cannot remove yourself.'}, status=status.HTTP_403_FORBIDDEN)

    # Prevent lower roles from removing admins
    if target_membership.role == 'admin' and requester_membership.role != 'admin':
        return Response({'error': 'Only admins can remove other admins.'}, status=status.HTTP_403_FORBIDDEN)

    # Prevent members from removing anyone
    if requester_membership.role == 'member':
        return Response({'error': 'You do not have permission to remove members.'}, status=status.HTTP_403_FORBIDDEN)

    target_membership.delete()
    return Response({'message': f'{username} removed from the club.'})

class ClubMemberRoleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, club_name, username):
        try:
            club = Club.objects.get(name=club_name)
            target_membership = ClubMembership.objects.get(club=club, user__username=username)
            acting_membership = ClubMembership.objects.get(club=club, user=request.user)
        except (Club.DoesNotExist, ClubMembership.DoesNotExist):
            return Response({'error': 'Club or user not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Optional: Prevent non-admins from changing roles
        if acting_membership.role != 'admin':
            return Response({'error': 'Only admins can change roles.'}, status=status.HTTP_403_FORBIDDEN)

        new_role = request.data.get('role')
        if new_role not in ['member', 'mod', 'admin']:
            return Response({'error': 'Invalid role.'}, status=status.HTTP_400_BAD_REQUEST)

        target_membership.role = new_role
        target_membership.save()
        return Response({'message': f'{username} is now a {new_role}.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_clubs(request):
    user = request.user
    memberships = user.clubmembership_set.select_related('club')
    data = [
        {
            "name": m.club.name,
            "description": m.club.description,
            "role": m.role,
        }
        for m in memberships
    ]
    return Response(data)

class InviteUserToClubAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, club_name):
        club = get_object_or_404(Club, name=club_name)
        invitee_username = request.data.get('username')

        # Check permission
        membership = ClubMembership.objects.filter(user=request.user, club=club).first()
        if not membership or membership.role not in ['admin', 'moderator']:
            return Response({'error': 'Not authorized to invite users.'}, status=403)

        try:
            invitee = User.objects.get(username=invitee_username)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        if ClubMembership.objects.filter(user=invitee, club=club).exists():
            return Response({'error': 'User is already a member.'}, status=400)

        invite, created = ClubInvite.objects.get_or_create(club=club, invitee=invitee, defaults={'invited_by': request.user})

        if not created:
            return Response({'message': 'User already invited.'})

        

        return Response({'message': 'Invite sent successfully.'}, status=201)

class AcceptInviteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, invite_id):
        invite = get_object_or_404(ClubInvite, id=invite_id, invitee=request.user)

        if invite.accepted:
            return Response({'message': 'Invite already accepted.'}, status=400)

        # ✅ Check before creating membership
        if not ClubMembership.objects.filter(user=request.user, club=invite.club).exists():
            ClubMembership.objects.create(user=request.user, club=invite.club, role='member')

        invite.accepted = True
        invite.save()

        # ✅ Also safe to call (won't duplicate due to get_or_create inside)
        from .utils import add_user_to_club_chat
        add_user_to_club_chat(invite.club, request.user)

        return Response({'message': 'You have joined the club!'}, status=200)

class ListClubInvitesAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClubInviteSerializer

    def get_queryset(self):
        return ClubInvite.objects.filter(invitee=self.request.user, accepted=False)

class RejectInviteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, invite_id):
        invite = get_object_or_404(ClubInvite, id=invite_id, invitee=request.user, accepted=False)
        invite.delete()
        return Response({'message': 'Invite rejected.'}, status=200)
