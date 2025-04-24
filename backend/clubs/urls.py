from django.urls import path
from . import views
from .views import update_member_role, remove_member

urlpatterns = [
    path('create/', views.ClubCreateAPIView.as_view(), name='club-create'),
    path('', views.ClubListAPIView.as_view(), name='club-list'),
    path('<str:club_name>/join/', views.ClubJoinAPIView.as_view(), name='club-join'),
    path('<str:club_name>/leave/', views.ClubLeaveAPIView.as_view(), name='club-leave'),
    path('<str:club_name>/profile/', views.ClubDetailAPIView.as_view(), name='club-detail'),
    path('<str:club_name>/delete/', views.ClubDeleteAPIView.as_view(), name='club-delete'),
    path('<str:club_name>/update-role/', update_member_role, name='update-member-role'),
    path('<str:club_name>/remove-member/', remove_member, name='remove-member'),
    path('<str:club_name>/members/<str:username>/', views.ClubMemberRoleAPIView.as_view(), name='club-member-role'),
]