from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Address

User = get_user_model()


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'long',
        'lat'
    ]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        "full_name",
        "project_name",
        "category",
        "phone_number",
        "profile_photo",
        "role",
        "is_active",
        "is_staff",
        "created_time",
    ]
    fieldsets = (
        (None, {"fields": ("full_name", "project_name", "category", "phone_number", "password", "role")}),
        (
            "Personal info",
            {
                "fields": (
                    "profile_photo",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("created_time",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "full_name",
                    "project_name",
                    "category",
                    "password1",
                    "password2",
                    "role",
                    "is_staff",
                ),
            },
        ),
    )
    search_fields = ("full_name", "phone_number")
    ordering = ("phone_number",)
    readonly_fields = ('created_time',)
