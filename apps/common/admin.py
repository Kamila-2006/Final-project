from django.contrib import admin
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title']
    search_fields = ['slug', 'title']
    exclude = ['slug']