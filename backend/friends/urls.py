from django.urls import path
from .views import FriendRequestCreateAPIView, FriendRequestListAPIView, FriendListAPIView, AcceptFriendRequestAPIView, RejectFriendRequestAPIView, NotificationListAPIView, CancelFriendRequestAPIView

urlpatterns = [
    path('send/', FriendRequestCreateAPIView.as_view(), name='friend-request-send'),
    path('requests/', FriendRequestListAPIView.as_view(), name='friend-request-list'),
    path('friends/', FriendListAPIView.as_view(), name='friend-list'),
    path('accept/', AcceptFriendRequestAPIView.as_view(), name='friend-request-accept'),
    path('reject/', RejectFriendRequestAPIView.as_view(), name='friend-request-reject'),
    path('notifications/', NotificationListAPIView.as_view(), name='notification-list'),
    path('cancel/', CancelFriendRequestAPIView.as_view(), name='friend-request-cancel'),
]