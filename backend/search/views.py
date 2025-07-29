from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from users.models import User
from clubs.models import Club
from events.models import Event
from users.serializers import UserPublicSerializer
from clubs.serializers import ClubSerializer
from events.serializers import EventSerializer
from courses.models import ClassInfo
from courses.serializers import ClassInfoSerializer

class GlobalSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query is required'}, status=400)

        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(full_name__icontains=query)
        )[:5]

        clubs = Club.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )[:5]

        events = Event.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query)
        )[:5]

        classes = ClassInfo.objects.filter(
            Q(descr__icontains=query) |
            Q(full_name__icontains=query)
        )[:5]

        return Response({
            'users': UserPublicSerializer(users, many=True, context={'request': request}).data,
            'clubs': ClubSerializer(clubs, many=True).data,
            'events': EventSerializer(events, many=True).data,
            'classes': ClassInfoSerializer(classes, many=True).data,
        })