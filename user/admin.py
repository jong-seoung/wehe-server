from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import UserImage


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "name", "nickname", "birthday", "is_staff",)
    list_filter = ("email", "name", "nickname", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("name", "nickname", "birthday", "user_image", "skills", "roles")},
        ),
        ("Permissions", {"fields": ("is_staff",)}),
    )

    search_fields = ("email", "name", "nickname")
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserImage)
