from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from clubs.models import Club, ClubMembership

User = get_user_model()
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='posts')
    club = models.ForeignKey(Club, null=True, blank=True, on_delete=models.CASCADE, related_name='posts')
    is_anonymous = models.BooleanField(default=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # For replies (optional, recursive relation)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    class Meta:
        ordering = ['-created_at']

    def can_post_in_club(self, user):
        if not self.club:
            return True
        membership = ClubMembership.objects.filter(user=user, club=self.club).first()
        return membership and membership.role in ['moderator', 'admin']

    def save(self, *args, **kwargs):
        if self.club:
            # Enforce that only moderators/admins can post in a club
            if not self.can_post_in_club(self.author):
                raise PermissionError("User is not allowed to post in this club.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{'Anonymous' if self.is_anonymous else self.author.username}: {self.content[:30]}"

    def visible_to_user(self, user):
        # Logic to check if a post is visible to a given user
        # For club posts: user must be a member (optional based on club privacy)
        if self.club:
            membership = ClubMembership.objects.filter(user=user, club=self.club).first()
            if self.club.is_private and not membership:
                return False
        # For posts by users, show only if author is user or friend, or post is public
        if not self.club and not self.is_anonymous:
            if self.author == user or self.author in user.friends:
                return True
            return False
        return True

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # one like per user per post

    def __str__(self):
        return f"{self.user.username} likes Post {self.post.id}"

class Repost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reposts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reposts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # one repost per user per post

    def __str__(self):
        return f"{self.user.username} reposted Post {self.post.id}"