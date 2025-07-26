from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import Category, Ad, AdPhoto


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ['name', 'icon', 'products_count']


@admin.register(Ad)
class AdAdmin(TabbedTranslationAdmin):
    list_display = ['name', 'slug', 'category', 'description', 'price']