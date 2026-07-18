from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import PasswordResetOTP, User


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'name', 'phone', 'is_staff', 'is_active']
    search_fields = ['email', 'name', 'phone']

    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone', 'address')}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'name', 'password1', 'password2'),
            },
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.register(PasswordResetOTP)