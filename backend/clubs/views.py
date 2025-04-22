from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Club, ClubMembership
from .serializers import ClubSerializer, ClubMembershipSerializer
from django.db.models import Q
from rest_framework.views import APIView

class ClubCreateAPIView(generics.GenericAPIView):
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            club = serializer.save(owner=request.user)
            ClubMembership.objects.create(user=request.user, club=club)
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
        try:
            club = Club.objects.get(name=club_name)
        except Club.DoesNotExist:
            return Response({'error': 'Club not found.'}, status=status.HTTP_404_NOT_FOUND)

        membership, created = ClubMembership.objects.get_or_create(user=request.user, club=club)

        if not created:
            return Response({'message': 'Already a member.'}, status=status.HTTP_200_OK)

        return Response({'message': f'Joined {club.name} successfully!'}, status=status.HTTP_201_CREATED)

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