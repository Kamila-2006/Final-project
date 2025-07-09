from django.contrib import admin
from .models import Page, Setting


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'created_time', 'updated_time']
    search_fields = ['slug', 'title', 'content']
    exclude = ['slug']

@admin.register(Setting)
class CommonSettingsAdmin(admin.ModelAdmin):
    list_display = ['phone', 'support_email', 'working_hours', 'app_version', 'maintenance_code']