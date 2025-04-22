from django.urls import path
from .views import (
    NotificationListAPIView,
    MarkNotificationsReadAPIView,
    ClearNotificationsAPIView,
    mark_single_notification_read,
)

urlpatterns = [
    path('', NotificationListAPIView.as_view(), name='notification-list'),
    path('mark-read/', MarkNotificationsReadAPIView.as_view(), name='notification-mark-read'),
    path('clear/', ClearNotificationsAPIView.as_view(), name='notification-clear'),
    path('<int:notif_id>/mark-read/', mark_single_notification_read, name='notification-mark-single-read'),
]