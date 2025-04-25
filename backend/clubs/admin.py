from django.contrib import admin
from .models import Club, ClubMembership, ClubInvite

# Inline for members
class ClubMembershipInline(admin.TabularInline):
    model = ClubMembership
    extra = 1  # How many empty rows to show for adding new members
    autocomplete_fields = ['user']
    fields = ('user', 'role', 'joined_at')
    readonly_fields = ('joined_at',)

# Inline for invites
class ClubInviteInline(admin.TabularInline):
    model = ClubInvite
    extra = 1
    autocomplete_fields = ['invitee', 'invited_by']
    fields = ('invitee', 'invited_by', 'accepted', 'created_at')
    readonly_fields = ('created_at',)

# Main club admin with inlines
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_verified', 'is_private', 'created_at', 'member_count')
    list_filter = ('is_verified', 'is_private', 'created_at')
    search_fields = ('name', 'description', 'owner__username')
    inlines = [ClubMembershipInline, ClubInviteInline]

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'

admin.site.register(Club, ClubAdmin)