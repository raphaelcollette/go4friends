from django.urls import path
from .views import signup, me, update_me, MyTokenObtainPairView

urlpatterns = [
    path('signup/', signup),
    path('login/', MyTokenObtainPairView.as_view()),
    path('me/', me),
    path('me/update/', update_me),
]