from django.urls import path
from .views import (
    ThreadListAPIView,
    ThreadDetailAPIView,
    MessageListAPIView,
    SendMessageAPIView,
    StartPrivateThreadAPIView,
    TogglePinMessageAPIView,
    get_or_create_class_thread
)

urlpatterns = [
    path('threads/', ThreadListAPIView.as_view(), name='thread-list'),                    # List all threads
    path('threads/<int:pk>/', ThreadDetailAPIView.as_view(), name='thread-detail'),       # Thread details
    path('threads/<int:thread_id>/messages/', MessageListAPIView.as_view(), name='message-list'),  # Messages in a thread
    path('threads/<int:thread_id>/send/', SendMessageAPIView.as_view(), name='send-message'),       # Send message to thread
    path('threads/start-private/', StartPrivateThreadAPIView.as_view(), name='start-private-thread'), # Start private DM
    path('messages/<int:pk>/pin/', TogglePinMessageAPIView.as_view(), name='toggle-pin-message'),
    path('class-thread/', get_or_create_class_thread, name='get_or_create_class_thread'),
]
