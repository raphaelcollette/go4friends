from django.urls import path
from .views import (
    FriendRequestCreateAPIView,
    FriendRequestListAPIView,
    FriendListAPIView,
    AcceptFriendRequestAPIView,
    RejectFriendRequestAPIView,
    NotificationListAPIView,
    CancelFriendRequestAPIView,
    MarkNotificationsReadAPIView,
    ClearNotificationsAPIView,
    RemoveFriendAPIView
)

urlpatterns = [
    path('send/', FriendRequestCreateAPIView.as_view(), name='friend-request-send'),
    path('requests/', FriendRequestListAPIView.as_view(), name='friend-request-list'),
    path('accept/', AcceptFriendRequestAPIView.as_view(), name='friend-request-accept'),
    path('reject/', RejectFriendRequestAPIView.as_view(), name='friend-request-reject'),
    path('cancel/', CancelFriendRequestAPIView.as_view(), name='friend-request-cancel'),

    path('friends/', FriendListAPIView.as_view(), name='friend-list'),
    path('remove/', RemoveFriendAPIView.as_view(), name='friend-remove'),
    
    path('notifications/', NotificationListAPIView.as_view(), name='notification-list'),
    path('notifications/read/', MarkNotificationsReadAPIView.as_view()),
    path('notifications/clear/', ClearNotificationsAPIView.as_view()),
]