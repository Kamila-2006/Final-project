from django.contrib import admin
from .models import Page, Setting, Region, District
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Page)
class PageAdmin(TabbedTranslationAdmin):
    list_display = ['slug', 'title', 'created_time', 'updated_time']
    search_fields = ['slug', 'title', 'content']

@admin.register(Setting)
class CommonSettingsAdmin(TabbedTranslationAdmin):
    list_display = ['phone', 'support_email', 'working_hours', 'app_version', 'maintenance_code']

@admin.register(Region)
class RegionAdmin(TabbedTranslationAdmin):
    list_display = ['name']

@admin.register(District)
class DistrictAdmin(TabbedTranslationAdmin):
    list_display = ['name']