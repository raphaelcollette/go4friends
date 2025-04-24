from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.EventCreateAPIView.as_view(), name='event-create'),
    path('', views.EventListAPIView.as_view(), name='event-list'),
    path('club/<str:club_name>/', views.ClubEventListAPIView.as_view(), name='club-event-list'),
    path('<int:event_id>/rsvp/', views.rsvp_event, name='event-rsvp'),
    path('<int:event_id>/cancel-rsvp/', views.cancel_rsvp, name='event-cancel-rsvp'),
    path('<int:event_id>/delete/', views.delete_event, name='delete-event'),
]
