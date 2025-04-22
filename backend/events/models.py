from django.db import models
from clubs.models import Club  # Link to Club if needed
from django.contrib.auth import get_user_model

User = get_user_model()


class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    attendees = models.ManyToManyField(User, related_name='attending_events', blank=True)

    def __str__(self):
        if self.club:
            return f"{self.title} (Club: {self.club.name})"
        return f"{self.title} (School-Wide Event)"
