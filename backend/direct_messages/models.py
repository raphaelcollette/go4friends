from django.db import models
from django.contrib.auth import get_user_model
from encrypted_model_fields.fields import EncryptedTextField

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = message = EncryptedTextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']  # newest first

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.message[:30]}"