from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    ordering = ("username", )
    list_display = (
        "full_name",
        "username",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_filter = ("date_joined", "is_active", "is_staff", "is_superuser")
    fieldsets = (
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "username", "password")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                    "groups",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("username", "first_name", "last_name")
    filter_horizontal = ("user_permissions", "groups")
    list_per_page = 20


admin.site.register(CustomUser, CustomUserAdmin)
