from django.urls import path
from .views import (
    NotificationListAPIView,
    MarkNotificationsReadAPIView,
    ClearNotificationsAPIView,
)

urlpatterns = [
    path('', NotificationListAPIView.as_view(), name='notification-list'),
    path('mark-read/', MarkNotificationsReadAPIView.as_view(), name='notification-mark-read'),
    path('clear/', ClearNotificationsAPIView.as_view(), name='notification-clear'),
]