from django.urls import path
from .views import signup, me, update_me, MyTokenObtainPairView, search_users, get_user_by_username
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', signup),
    path('login/', MyTokenObtainPairView.as_view()),
    path('me/', me),
    path('me/update/', update_me),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', search_users),
    path('profile/<str:username>/', get_user_by_username),
]