from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.list_posts, name='list_posts'),
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('<int:post_id>/unlike/', views.unlike_post, name='unlike_post'),
    path('<int:post_id>/repost/', views.repost_post, name='repost_post'),
    path('<int:post_id>/undo_repost/', views.undo_repost, name='undo_repost'),
    path('user/<str:username>/', views.list_user_posts, name='list_user_posts'),
    path('<int:post_id>/', views.get_post_detail, name='get_post_detail'),

    # Replies endpoint (GET replies for a post)
    path('<int:post_id>/replies/', views.list_post_replies, name='list_post_replies'),
] 