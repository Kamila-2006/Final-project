from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import Category


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ['name', 'icon', 'products_count']