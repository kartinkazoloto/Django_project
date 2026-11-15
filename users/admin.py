from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'phone_number',
                'avatar',
                'country',
                'date_of_birth',
                'bio'
            )
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'phone_number',
                'country'
            ),
        }),
    )

    list_display = (
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'country',
        'is_staff',
        'is_active'
    )

    list_filter = ('is_staff', 'is_active', 'is_superuser', 'country')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'country')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')