from django.urls import path
from .views import (
    ThreadListAPIView,
    ThreadDetailAPIView,
    MessageListAPIView,
    SendMessageAPIView,
    StartPrivateThreadAPIView,
)

urlpatterns = [
    path('threads/', ThreadListAPIView.as_view(), name='thread-list'),                    # List all threads
    path('threads/<int:pk>/', ThreadDetailAPIView.as_view(), name='thread-detail'),       # Thread details
    path('threads/<int:thread_id>/messages/', MessageListAPIView.as_view(), name='message-list'),  # Messages in a thread
    path('threads/<int:thread_id>/send/', SendMessageAPIView.as_view(), name='send-message'),       # Send message to thread
    path('threads/start-private/', StartPrivateThreadAPIView.as_view(), name='start-private-thread'), # Start private DM
]
