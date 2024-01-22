from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset
    
    list_display = ("id", "username", "email")
    list_filter = ("email",)

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': (
                'first_name',
                'last_name', 'coin', 'phone')
        }),
        ('Permissions', {
            'fields': (
                'is_superuser',
                'groups', 'user_permissions')
        })
    )

    search_fields = ('email', 'first_name',"username")
    ordering = ('-id', 'email')
