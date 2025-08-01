from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import Category, Ad, AdPhoto


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ['name', 'icon', 'parent']
    list_filter = ('parent',)


@admin.register(Ad)
class AdAdmin(TabbedTranslationAdmin):
    list_display = ['name', 'slug', 'category', 'description', 'price']