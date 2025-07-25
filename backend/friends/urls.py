from django.urls import path
from .views import (
    FriendRequestCreateAPIView,
    FriendRequestListAPIView,
    FriendListAPIView,
    AcceptFriendRequestAPIView,
    RejectFriendRequestAPIView,
    CancelFriendRequestAPIView,
    RemoveFriendAPIView,
    friend_suggestions,
    UserFriendsCountAPIView,
)

urlpatterns = [
    path('send/', FriendRequestCreateAPIView.as_view(), name='friend-request-send'),
    path('requests/', FriendRequestListAPIView.as_view(), name='friend-request-list'),
    path('accept/', AcceptFriendRequestAPIView.as_view(), name='friend-request-accept'),
    path('reject/', RejectFriendRequestAPIView.as_view(), name='friend-request-reject'),
    path('cancel/', CancelFriendRequestAPIView.as_view(), name='friend-request-cancel'),

    path('suggestions/', friend_suggestions, name='friend-suggestions'),
    
    path('friends/', FriendListAPIView.as_view(), name='friend-list'),
    path('remove/', RemoveFriendAPIView.as_view(), name='friend-remove'),
    path('<str:username>/count/', UserFriendsCountAPIView.as_view(), name='user_friends_count'),
    
]