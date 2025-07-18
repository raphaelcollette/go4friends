from django.urls import path
from . import views
from .views import update_member_role, remove_member, my_clubs

urlpatterns = [
    # Club CRUD
    path('create/', views.ClubCreateAPIView.as_view(), name='club-create'),
    path('', views.ClubListAPIView.as_view(), name='club-list'),
    path('<str:club_name>/profile/', views.ClubDetailAPIView.as_view(), name='club-detail'),
    path('<str:club_name>/delete/', views.ClubDeleteAPIView.as_view(), name='club-delete'),

    # Membership actions
    path('<str:club_name>/join/', views.ClubJoinAPIView.as_view(), name='club-join'),
    path('<str:club_name>/leave/', views.ClubLeaveAPIView.as_view(), name='club-leave'),
    path('<str:club_name>/update-role/', views.update_member_role, name='update-member-role'),
    path('<str:club_name>/remove-member/', views.remove_member, name='remove-member'),
    path('<str:club_name>/members/<str:username>/', views.ClubMemberRoleAPIView.as_view(), name='club-member-role'),

    # User-specific clubs
    path('my/', views.my_clubs, name='my-clubs'),

    # Invite system
    path('<str:club_name>/invite/', views.InviteUserToClubAPIView.as_view(), name='club-invite'),
    path('invites/', views.ListClubInvitesAPIView.as_view(), name='list-invites'),
    path('invites/<int:invite_id>/accept/', views.AcceptInviteAPIView.as_view(), name='accept-invite'),
    path('invites/<int:invite_id>/reject/', views.RejectInviteAPIView.as_view(), name='reject-invite'),

    path('suggested/', views.SuggestedClubsAPIView.as_view(), name='suggested-clubs'),
]