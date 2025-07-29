# posts/views.py
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Like, Repost
from clubs.models import ClubMembership
from django.contrib.auth import get_user_model
from posts.serializers import PostSerializer
from better_profanity import profanity
from rest_framework.throttling import UserRateThrottle
from django.db.models import Q, Count, Exists, OuterRef, Subquery
from django.http import JsonResponse
from django.utils.timesince import timesince
from django.utils.timezone import now

User = get_user_model()
profanity.load_censor_words()

class CreatePostThrottle(UserRateThrottle):
    rate = '10/hour'

class DeletePostThrottle(UserRateThrottle):
    rate = '30/hour'

class LikePostThrottle(UserRateThrottle):
    rate = '60/hour'

class UnlikePostThrottle(UserRateThrottle):
    rate = '60/hour'

class RepostThrottle(UserRateThrottle):
    rate = '30/hour'

class UndoRepostThrottle(UserRateThrottle):
    rate = '30/hour'

class ListPostsThrottle(UserRateThrottle):
    rate = '100/hour'

class ListUserPostsThrottle(UserRateThrottle):
    rate = '100/hour'

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
#@throttle_classes([CreatePostThrottle])
def create_post(request):
    user = request.user
    club_id = request.data.get('club')
    content = request.data.get('content', '').strip()
    is_anonymous = request.data.get('is_anonymous', False)
    parent_id = request.data.get('parent')

    if profanity.contains_profanity(content):
        return Response({"detail": "Profanity detected in post content."}, status=status.HTTP_400_BAD_REQUEST)

    club = None
    if club_id:
        club = get_object_or_404(ClubMembership.model.club.field.related_model, id=club_id)
        membership = ClubMembership.objects.filter(user=user, club=club).first()
        if not membership or membership.role not in ['moderator', 'admin']:
            return Response({"detail": "No permission to post in this club."}, status=status.HTTP_403_FORBIDDEN)

    parent = None
    if parent_id:
        parent = get_object_or_404(Post, id=parent_id)

    post = Post(
        author=user,
        club=club,
        content=content,
        is_anonymous=is_anonymous,
        parent=parent,
    )
    try:
        post.save()
    except PermissionError:
        return Response({"detail": "Permission denied for posting."}, status=status.HTTP_403_FORBIDDEN)

    serializer = PostSerializer(post, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
#@throttle_classes([DeletePostThrottle])
def delete_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    if post.club:
        membership = ClubMembership.objects.filter(user=user, club=post.club).first()
        if not membership or membership.role not in ['moderator', 'admin']:
            return Response({"detail": "No permission to delete this club post."}, status=status.HTTP_403_FORBIDDEN)
    else:
        if post.author != user:
            return Response({"detail": "Cannot delete others' posts."}, status=status.HTTP_403_FORBIDDEN)

    post.delete()
    return Response({"message": "Post deleted"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
#@throttle_classes([LikePostThrottle])
def like_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(user=user, post=post)
    if not created:
        return Response({"detail": "Already liked"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
#@throttle_classes([UnlikePostThrottle])
def unlike_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    like = Like.objects.filter(user=user, post=post).first()
    if not like:
        return Response({"detail": "Like does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    like.delete()
    return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
#@throttle_classes([RepostThrottle])
def repost_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    repost, created = Repost.objects.get_or_create(user=user, post=post)
    if not created:
        return Response({"detail": "Already reposted"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Post reposted"}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
#@throttle_classes([UndoRepostThrottle])
def undo_repost(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    repost = Repost.objects.filter(user=user, post=post).first()
    if not repost:
        return Response({"detail": "Repost does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    repost.delete()
    return Response({"message": "Repost removed"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
#@throttle_classes([ListPostsThrottle])
def list_posts(request):
    user = request.user
    try:
        likes_subquery = Like.objects.filter(post=OuterRef('pk'), user=user)
        reposts_subquery = Repost.objects.filter(post=OuterRef('pk'), user=user)

        posts = Post.objects.filter(parent__isnull=True).annotate(
            comment_count=Count('replies', distinct=True),
            like_count=Count('likes', distinct=True),
            repost_count=Count('reposts', distinct=True),
            has_liked=Exists(likes_subquery),
            has_reposted=Exists(reposts_subquery),
            reposted_by_username=Subquery(
                Repost.objects.filter(post=OuterRef('pk'), user=user).values('user__username')[:1]
            ),
        ).select_related('author').order_by('-created_at')[:50]

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({"detail": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
#@throttle_classes([ListUserPostsThrottle])
def list_user_posts(request, username):
    user = request.user

    likes_subquery = Like.objects.filter(post=OuterRef('pk'), user=user)
    reposts_subquery = Repost.objects.filter(post=OuterRef('pk'), user=user)

    posts = Post.objects.filter(
        Q(author__username=username) | Q(reposts__user__username=username),
        parent__isnull=True,
        is_anonymous=False,
    ).distinct().annotate(
        comment_count=Count('replies', distinct=True),
        like_count=Count('likes', distinct=True),
        repost_count=Count('reposts', distinct=True),
        has_liked=Exists(likes_subquery),
        has_reposted=Exists(reposts_subquery),
        reposted_by_username=Subquery(
            Repost.objects.filter(post=OuterRef('pk'), user=user).values('user__username')[:1]
        ),
    ).select_related('author').order_by('-created_at')

    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_post_detail(request, post_id):
    user = request.user

    likes_subquery = Like.objects.filter(post=OuterRef('pk'), user=user)
    reposts_subquery = Repost.objects.filter(post=OuterRef('pk'), user=user)

    post = get_object_or_404(Post.objects.annotate(
        comment_count=Count('replies', distinct=True),
        like_count=Count('likes', distinct=True),
        repost_count=Count('reposts', distinct=True),
        has_liked=Exists(likes_subquery),
        has_reposted=Exists(reposts_subquery),
        reposted_by_username=Subquery(
            Repost.objects.filter(post=OuterRef('pk'), user=user).values('user__username')[:1]
        ),
    ).select_related('author'), id=post_id)

    serializer = PostSerializer(post, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_post_replies(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    replies = post.replies.select_related('author').order_by('created_at')
    current_time = now()

    data = [
        {
            'id': reply.id,
            'authorName': reply.author.username if not reply.is_anonymous else 'Anonymous',
            'username': reply.author.username if not reply.is_anonymous else None,
            'authorInitials': ''.join([n[0].upper() for n in reply.author.username.split()]) if not reply.is_anonymous else 'A',
            'content': reply.content,
            'timeAgo': timesince(reply.created_at, current_time) + ' ago',
            'is_anonymous': reply.is_anonymous,
            'parent_id': reply.parent.id if reply.parent else None,
        }
        for reply in replies
    ]
    return JsonResponse(data, safe=False)