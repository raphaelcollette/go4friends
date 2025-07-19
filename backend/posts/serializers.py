from rest_framework import serializers, viewsets
from django.utils.timesince import timesince
from django.db.models import Count, Exists, OuterRef, Subquery
from .models import Post, Like, Repost
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'profile_picture_url']

class PostSerializer(serializers.ModelSerializer):
    authorName = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    authorInitials = serializers.SerializerMethodField()
    timeAgo = serializers.SerializerMethodField()
    commentCount = serializers.IntegerField(source='comment_count', read_only=True)
    likeCount = serializers.IntegerField(source='like_count', read_only=True)
    repostCount = serializers.IntegerField(source='repost_count', read_only=True)
    hasLiked = serializers.BooleanField(source='has_liked', read_only=True)
    hasReposted = serializers.BooleanField(source='has_reposted', read_only=True)
    reposted_by = serializers.CharField(source='reposted_by_username', read_only=True)
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSummarySerializer(source='author', read_only=True)
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'authorName', 'username', 'authorInitials', 'content', 'timeAgo',
            'commentCount', 'likeCount', 'repostCount', 'hasLiked', 'hasReposted',
            'is_anonymous', 'reposted_by', 'parent', 'user', 'author_username',
        ]

    def get_authorName(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        full_name = getattr(obj.author, 'full_name', None)
        return full_name if full_name else obj.author.username

    def get_username(self, obj):
        if obj.is_anonymous:
            return "anonymous"
        return obj.author.username

    def get_authorInitials(self, obj):
        if obj.is_anonymous:
            return "AN"
        name = getattr(obj.author, 'full_name', None) or obj.author.username
        parts = name.split()
        initials = "".join([p[0].upper() for p in parts[:2]])
        return initials or "U"

    def get_timeAgo(self, obj):
        return timesince(obj.created_at).split(',')[0] + " ago"

    def get_author_username(self, obj):
        request = self.context.get('request')
        if obj.author and request and request.user == obj.author:
            return obj.author.username
        return None

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user

        likes_subquery = Like.objects.filter(post=OuterRef('pk'), user=user)
        reposts_subquery = Repost.objects.filter(post=OuterRef('pk'), user=user)

        return Post.objects.filter(parent__isnull=True, club__isnull=True).annotate(
            comment_count=Count('replies', distinct=True),
            like_count=Count('likes', distinct=True),
            repost_count=Count('reposts', distinct=True),
            has_liked=Exists(likes_subquery),
            has_reposted=Exists(reposts_subquery),
            reposted_by_username=Subquery(
                Repost.objects.filter(post=OuterRef('pk'), user=user).values('user__username')[:1]
            ),
        ).select_related('author').order_by('-created_at')
