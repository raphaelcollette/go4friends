from django.urls import path
from .views import SendMessageAPIView, ThreadAPIView

urlpatterns = [
    path('send/', SendMessageAPIView.as_view(), name='send-message'),
    path('thread/', ThreadAPIView.as_view(), name='message-thread'),
]
