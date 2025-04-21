from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.EventCreateAPIView.as_view(), name='event-create'),
    path('', views.EventListAPIView.as_view(), name='event-list'),
    path('club/<str:club_name>/', views.ClubEventListAPIView.as_view(), name='club-event-list'),
]
