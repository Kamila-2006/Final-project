from modeltranslation.translator import register, TranslationOptions
from .models import User


@register(User)
class SellerTranslationOptions(TranslationOptions):
    fields = ('full_name', )