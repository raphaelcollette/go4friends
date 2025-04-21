from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.ClubCreateAPIView.as_view(), name='club-create'),
    path('', views.ClubListAPIView.as_view(), name='club-list'),
    path('<str:club_name>/join/', views.ClubJoinAPIView.as_view(), name='club-join'),
    path('<str:club_name>/leave/', views.ClubLeaveAPIView.as_view(), name='club-leave'),
]