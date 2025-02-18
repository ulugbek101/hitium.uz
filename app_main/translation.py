from modeltranslation.translator import register, TranslationOptions
from .models import Service

@register(Service)
class BookTranslationOptions(TranslationOptions):
	fields = ('name', 'description', 'slug')