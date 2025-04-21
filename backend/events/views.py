from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Event
from .serializers import EventSerializer
from clubs.models import Club

class EventCreateAPIView(generics.GenericAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        club_name = request.data.get('club_name')
        club = None

        if club_name:
            try:
                club = Club.objects.get(name=club_name)
            except Club.DoesNotExist:
                return Response({'error': 'Club not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(club=club)
            return Response(EventSerializer(event, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated] 
    ordering_fields = ['date', 'title']
    ordering = ['date']

    def get_queryset(self):
        queryset = Event.objects.all()
        query = self.request.GET.get('q')
        upcoming = self.request.GET.get('upcoming')

        if query:
            queryset = queryset.filter(title__icontains=query)

        if upcoming == 'true':
            queryset = queryset.filter(date__gte=timezone.now())

        return queryset

class ClubEventListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated] 
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
