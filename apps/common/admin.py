from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import District, Page, Region, Setting


@admin.register(Page)
class PageAdmin(TabbedTranslationAdmin):
    list_display = ["slug", "title", "created_time", "updated_time"]
    search_fields = ["slug", "title", "content"]


@admin.register(Setting)
class CommonSettingsAdmin(TabbedTranslationAdmin):
    list_display = [
        "phone",
        "support_email",
        "working_hours",
        "app_version",
        "maintenance_code",
    ]

    def has_add_permission(self, request):
        if Setting.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Region)
class RegionAdmin(TabbedTranslationAdmin):
    list_display = ["name"]
    search_fields = ("name",)


@admin.register(District)
class DistrictAdmin(TabbedTranslationAdmin):
    list_display = ["name"]
    search_fields = ("name",)
    list_filter = ["region"]
