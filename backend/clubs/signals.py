from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ClubInvite
from notifications.models import Notification

@receiver(post_save, sender=ClubInvite)
def create_club_invite_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.invitee,
            type='club_invite',
            message=f"You've been invited to join {instance.club.name}!"
        )