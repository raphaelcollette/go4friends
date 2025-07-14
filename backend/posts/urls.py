from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('<int:post_id>/unlike/', views.unlike_post, name='unlike_post'),
    path('<int:post_id>/repost/', views.repost_post, name='repost_post'),
    path('<int:post_id>/undo_repost/', views.undo_repost, name='undo_repost'),
] + router.urls