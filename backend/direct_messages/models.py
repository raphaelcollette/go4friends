from django.db import models
from django.contrib.auth import get_user_model
from encrypted_model_fields.fields import EncryptedTextField

User = get_user_model()

class Thread(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  # Optional, used for group chats
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class_info = models.ForeignKey('courses.ClassInfo', null=True, blank=True, on_delete=models.SET_NULL, related_name='threads')

    def __str__(self):
        return self.name or f"Thread {self.id}"

class ThreadParticipant(models.Model):
    thread = models.ForeignKey(Thread, related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('thread', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.thread}"

class Message(models.Model):
    thread = models.ForeignKey(Thread, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = EncryptedTextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.message[:30]}"
