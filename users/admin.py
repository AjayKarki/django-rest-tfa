from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(UserAdmin):
    readonly_fields = ["created_at", "updated_at", "last_login", "deleted_at"]
    list_display = ("name", "email", "created_at")
    list_filter = ("created_at", "is_active",)
    search_fields = ("name",)
    ordering = ("-id",)

    fieldsets = (
        (None, {"fields": ("email" , "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'name', 'password1', 'password2')}),
    )
