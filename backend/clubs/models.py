from django.db import models
from django.contrib.auth import get_user_model
from direct_messages.models import Thread

User = get_user_model()

class Club(models.Model):
    """
    Represents a user-created club. Each club has a unique name, an owner,
    and can be private or verified. Clubs also have a dedicated message thread.
    """
    name = models.CharField(max_length=100, unique=True)  # Unique name for the club
    description = models.TextField(blank=True)  # Optional description
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_clubs')  # Club creator
    members = models.ManyToManyField(User, through='ClubMembership', related_name='clubs')  # Members via membership table
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
    is_verified = models.BooleanField(default=False)  # Admin or system verification flag
    is_private = models.BooleanField(default=False)  # Whether the club is invite-only
    thread = models.OneToOneField(Thread, null=True, blank=True, on_delete=models.SET_NULL, related_name="club")  # Optional associated DM thread

    def __str__(self):
        return self.name


class ClubMembership(models.Model):
    """
    Intermediate model for users in clubs with assigned roles.
    A user can only be in a club once.
    """
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Member
    club = models.ForeignKey(Club, on_delete=models.CASCADE)  # Associated club
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')  # Role within the club
    joined_at = models.DateTimeField(auto_now_add=True)  # Timestamp of membership creation

    class Meta:
        unique_together = ('user', 'club')  # Prevent duplicate memberships

    def __str__(self):
        return f"{self.user.username} in {self.club.name}"


class ClubInvite(models.Model):
    """
    Tracks invitations for users to join a club.
    Only one pending invite per user per club is allowed.
    """
    club = models.ForeignKey(Club, on_delete=models.CASCADE)  # Club being invited to
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')  # Inviter
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='club_invites')  # Invitee
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of invite creation
    accepted = models.BooleanField(default=False)  # Whether the invite was accepted

    class Meta:
        unique_together = ('club', 'invitee')  # Prevent duplicate invites

    def __str__(self):
        return f"{self.invitee.username} invited to {self.club.name} by {self.invited_by.username}"
