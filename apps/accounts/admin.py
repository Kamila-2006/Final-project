from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Address

User = get_user_model()


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    max_num = 1
    can_delete = True


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        "full_name",
        "project_name",
        "category",
        "status",
        "phone_number",
        "profile_photo",
        "address_name",
        "region",
        "district",
        "role",
        "is_active",
        "is_staff",
        "created_time",
    ]

    def address_name(self, obj):
        return obj.address.name if hasattr(obj, "address") else "-"

    address_name.short_description = "Адрес"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "full_name",
                    "project_name",
                    "category",
                    "status",
                    "phone_number",
                    "password",
                    "role",
                    "address_name",
                    "region",
                    "district",
                )
            },
        ),
        (
            "Personal info",
            {"fields": ("profile_photo",)},
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
    readonly_fields = ("created_time", "address_name")
    inlines = [AddressInline]
