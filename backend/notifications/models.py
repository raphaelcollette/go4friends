from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('friend_request', 'Friend Request'),
        ('club_invite', 'Club Invite'),
        ('message', 'Message'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, blank=False, null=False)
    message = models.CharField(max_length=255)
    related_id = models.PositiveIntegerField(null=True, blank=True)  # ID of related object (optional)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.type}: {self.message}"