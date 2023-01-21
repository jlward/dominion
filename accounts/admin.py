from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from players.models import Player

from .models import User


class PlayerInline(admin.StackedInline):
    model = Player


class UserAdmin(UserAdmin):
    # Copied all of these from `UserAdmin` and replaced all instances of `username` with `email`.
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)

    inlines = [PlayerInline]


admin.site.register(User, UserAdmin)
