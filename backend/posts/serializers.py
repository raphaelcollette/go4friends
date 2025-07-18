from rest_framework import serializers, viewsets
from django.utils.timesince import timesince
from .models import Post
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
    commentCount = serializers.SerializerMethodField()
    likeCount = serializers.SerializerMethodField()
    repostCount = serializers.SerializerMethodField()
    hasLiked = serializers.SerializerMethodField()
    hasReposted = serializers.SerializerMethodField()
    reposted_by = serializers.SerializerMethodField()
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSummarySerializer(source='author', read_only=True)
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'authorName', 'username', 'authorInitials', 'content', 'timeAgo',
            'commentCount', 'likeCount', 'repostCount', 'hasLiked', 'hasReposted', 'is_anonymous', 'reposted_by', 'parent', 'user',
            'author_username',
        ]

    def get_authorName(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        full_name = getattr(obj.author, 'full_name', None)  # or use a field if exists
        if full_name:
            return full_name
        return obj.author.username

    def get_username(self, obj):
        if obj.is_anonymous:
            return "anonymous"
        return obj.author.username

    def get_authorInitials(self, obj):
        if obj.is_anonymous:
            return "AN"
        # Try full_name attribute first, fallback to username
        name = getattr(obj.author, 'full_name', None) or obj.author.username
        parts = name.split()
        initials = "".join([p[0].upper() for p in parts[:2]])
        return initials or "U"

    def get_timeAgo(self, obj):
        return timesince(obj.created_at).split(',')[0] + " ago"

    def get_commentCount(self, obj):
        return obj.replies.count()

    def get_likeCount(self, obj):
        return obj.likes.count()

    def get_repostCount(self, obj):
        return obj.reposts.count()

    def get_hasLiked(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.likes.filter(user=user).exists()

    def get_hasReposted(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.reposts.filter(user=user).exists()

    def get_reposted_by(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return None
        repost = obj.reposts.filter(user=user).first()
        if repost:
            return user.username
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_anonymous:
            data['user'] = None
        if data.get('author_username') is None:
            data.pop('author_username', None)
        return data

    def get_author_username(self, obj):
        request = self.context.get('request')
        if obj.author and request and request.user == obj.author:
            return obj.author.username
        return None

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(parent__isnull=True, club__isnull=True).order_by('-created_at')
    serializer_class = PostSerializer

    def get_serializer_context(self):
        return {'request': self.request}