from modeltranslation.translator import register, TranslationOptions
from .models import Region, District, Setting, Page


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(District)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Setting)
class SettingTranslationOptions(TranslationOptions):
    fields = ('working_hours',)


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'content')