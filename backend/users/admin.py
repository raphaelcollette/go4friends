from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        'email', 'username', 'full_name', 'major', 'graduation_year',
        'is_staff', 'is_active', 'is_private', 'created_at'
    )
    list_filter = ('is_staff', 'is_active', 'is_private', 'major', 'graduation_year')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {
            'fields': (
                'full_name', 'bio', 'location', 'major',
                'graduation_year', 'interests', 'profile_picture',
            )
        }),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_private', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'password1', 'password2',
                'full_name', 'major', 'graduation_year', 'is_staff', 'is_active', 'is_private'
            ),
        }),
    )

    search_fields = ('email', 'username', 'full_name', 'major')
    ordering = ('email',)
    readonly_fields = ('created_at',)  # prevent editing creation date

admin.site.register(User, CustomUserAdmin)
