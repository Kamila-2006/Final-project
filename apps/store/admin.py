from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Ad, AdPhoto, Category


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ["id", "name", "icon", "parent"]
    list_filter = ("parent",)


class AdPhotoInline(admin.TabularInline):
    model = AdPhoto
    extra = 1
    fields = ["image", "is_main", "created_at"]
    readonly_fields = ["created_at"]
    show_change_link = True


@admin.register(Ad)
class AdAdmin(TabbedTranslationAdmin):
    list_display = ["id", "name", "slug", "category", "description", "price", "main_photo"]
    inlines = [AdPhotoInline]

    def main_photo(self, obj):
        photo = obj.photos.filter(is_main=True).first()
        if photo and photo.image:
            return format_html('<img src="{}" style="height:50px;width:auto;" />', photo.image.url)
        return "—"

    main_photo.short_description = "Main Photo"
