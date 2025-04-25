from django.contrib import admin
from .models import Event
from django.utils.html import format_html

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'club_name', 'location', 'date', 'attendee_count', 'created_at', 'event_image_preview')
    list_filter = ('club', 'date', 'created_at')
    search_fields = ('title', 'description', 'location', 'club__name')
    readonly_fields = ('created_at', 'event_image_preview')
    autocomplete_fields = ['club', 'attendees']
    filter_horizontal = ('attendees',)

    def club_name(self, obj):
        return obj.club.name if obj.club else "School-Wide"
    club_name.short_description = 'Club'

    def attendee_count(self, obj):
        return obj.attendees.count()
    attendee_count.short_description = 'Attendees'

    def event_image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" style="max-height: 100px;" />')
        return "(No Image)"
    event_image_preview.short_description = 'Image Preview'

admin.site.register(Event, EventAdmin)