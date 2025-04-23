from django.urls import path
from .views import GlobalSearchAPIView

urlpatterns = [
    path('', GlobalSearchAPIView.as_view(), name='global-search'),
]