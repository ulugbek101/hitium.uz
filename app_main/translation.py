from modeltranslation.translator import register, TranslationOptions
from .models import Service, Project

@register(Service)
class BookTranslationOptions(TranslationOptions):
	fields = ('name', 'description', 'slug')



@register(Project)
class ProjectTranslationOptions(TranslationOptions):
	fields = ('name', 'description', 'slug')
