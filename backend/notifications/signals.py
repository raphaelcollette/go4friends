from django.db.models.signals import post_save
from django.dispatch import receiver
from friends.models import FriendRequest
from .models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=FriendRequest)
def friend_request_created(sender, instance, created, **kwargs):
    if created and instance.status == 'pending':
        # Create a notification for the recipient
        Notification.objects.create(
            user=instance.to_user,
            type='friend_request',
            message=f"{instance.from_user.username} sent you a friend request!"
        )

    elif not created and instance.status == 'accepted':
        # If a friend request was accepted later
        Notification.objects.create(
            user=instance.from_user,
            type='message',
            message=f"{instance.to_user.username} accepted your friend request!"
        )