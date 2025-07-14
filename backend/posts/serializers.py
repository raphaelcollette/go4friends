from rest_framework import serializers, viewsets
from django.utils.timesince import timesince
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    authorName = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    authorInitials = serializers.SerializerMethodField()
    timeAgo = serializers.SerializerMethodField()
    commentCount = serializers.SerializerMethodField()
    likeCount = serializers.SerializerMethodField()
    repostCount = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'authorName', 'username', 'authorInitials', 'content', 'timeAgo',
            'commentCount', 'likeCount', 'repostCount',
        ]

    def get_authorName(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        return obj.author.get_full_name() or obj.author.username

    def get_username(self, obj):
        if obj.is_anonymous:
            return "anonymous"
        return obj.author.username

    def get_authorInitials(self, obj):
        if obj.is_anonymous:
            return "AN"
        name = obj.author.get_full_name() or obj.author.username
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

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(parent__isnull=True).order_by('-created_at')
    serializer_class = PostSerializer