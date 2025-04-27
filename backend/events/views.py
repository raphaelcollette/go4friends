from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from .models import Event
from .serializers import EventSerializer
from clubs.models import Club
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.views import APIView
from clubs.models import ClubMembership
from users.serializers import UserPublicSerializer

# --- Create Event ---
class EventCreateAPIView(generics.GenericAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Needed for images

    def post(self, request, *args, **kwargs):
        club_name = request.data.get('club_name')
        club = None

        # If this is a club event, fetch the club and check if the user is allowed
        if club_name:
            try:
                club = Club.objects.get(name=club_name)
            except Club.DoesNotExist:
                return Response({'error': 'Club not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Check if the user is an admin or moderator in that club
            membership = club.clubmembership_set.filter(user=request.user).first()
            if not membership or membership.role not in ['admin', 'moderator']:
                return Response({'error': 'Only admins or moderators can create events for this club.'},
                                status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(club=club)
            return Response(EventSerializer(event, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- List All Events ---
class EventListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date', 'title']
    ordering = ['date']

    def get_queryset(self):
        user = self.request.user
        queryset = Event.objects.all()
        query = self.request.GET.get('q')
        upcoming = self.request.GET.get('upcoming')
        club_name = self.request.GET.get('club')
        rsvp = self.request.GET.get('rsvp')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        my_clubs = self.request.GET.get('my_clubs')

        if query:
            queryset = queryset.filter(title__icontains=query)

        if upcoming == 'true':
            queryset = queryset.filter(date__gte=timezone.now())

        if club_name:
            queryset = queryset.filter(club__name__iexact=club_name)

        if rsvp == 'true':
            queryset = queryset.filter(attendees=user)

        if my_clubs == 'true':
            # Get the clubs where the user is a member
            club_ids = user.clubmembership_set.values_list('club_id', flat=True)
            queryset = queryset.filter(club__id__in=club_ids)

        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset

# --- List Events by Club ---
class ClubEventListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date', 'title']
    ordering = ['date']

    def get_queryset(self):
        club_name = self.kwargs['club_name']
        queryset = Event.objects.filter(club__name=club_name)

        query = self.request.GET.get('q')
        upcoming = self.request.GET.get('upcoming')

        if query:
            queryset = queryset.filter(title__icontains=query)

        if upcoming == 'true':
            queryset = queryset.filter(date__gte=timezone.now())

        return queryset

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rsvp_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        event.attendees.add(request.user)
        return Response({'message': 'RSVP successful!'})
    except Event.DoesNotExist:
        return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_rsvp(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        event.attendees.remove(request.user)
        return Response({'message': 'RSVP cancelled.'})
    except Event.DoesNotExist:
        return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)

        # Only allow deletion if user is a moderator/admin of the club
        if event.club:
            membership = event.club.clubmembership_set.filter(user=request.user).first()
            if not membership or membership.role not in ['admin', 'moderator']:
                return Response({"error": "You don't have permission to delete this event."}, status=status.HTTP_403_FORBIDDEN)

        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except Event.DoesNotExist:
        return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)

        # Only allow update if user is admin/mod of the club
        if event.club:
            membership = event.club.clubmembership_set.filter(user=request.user).first()
            if not membership or membership.role not in ['admin', 'moderator']:
                return Response({"error": "You don't have permission to edit this event."},
                                status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Event.DoesNotExist:
        return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

class SuggestedEventsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        me = request.user

        my_club_ids = list(me.clubs.values_list('id', flat=True))
        my_interests = set(map(str.lower, me.interests or [])) if me.interests else set()
        my_friends = me.friends.all()

        # Start with all upcoming events
        events = Event.objects.filter(date__gte=timezone.now()).exclude(club__isnull=True) # assuming event has a 'date' and optional 'club'

        suggestions = []
        for event in events:
            reasons = []

            # If event is tied to a club I'm in
            if event.club and event.club.id in my_club_ids:
                reasons.append('Event hosted by your club')

            # If event matches interests by event title/description
            if my_interests:
                combined_text = (event.title + ' ' + (event.description or '')).lower()
                if any(interest in combined_text for interest in my_interests):
                    reasons.append('Matches your interests')

            # If my friends RSVP’d to the event (optional)
            friend_ids = my_friends.values_list('id', flat=True)
            friend_attendees = event.attendees.filter(id__in=friend_ids).count()
            if friend_attendees > 0:
                reasons.append(f'{friend_attendees} friend(s) attending')

            if reasons:
                event_data = {
                    'id': event.id,
                    'title': event.title,
                    'date': event.date,
                    'club': event.club.name if event.club else None,
                    'match_reasons': reasons,
                }
                suggestions.append(event_data)

        return Response(suggestions)

class EventDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

        attendees = event.attendees.all()
        attendee_data = UserPublicSerializer(attendees, many=True, context={'request': request}).data
        
        return Response({
            'event': EventSerializer(event, context={'request': request}).data,
            'attendees': attendee_data
        })