from django.contrib import admin
from .models import FriendRequest

# Register your models here.

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'status', 'created_at')