from modeltranslation.translator import register, TranslationOptions
from .models import Service, Project, ProjectImage, GalleryImage

@register(Service)
class BookTranslationOptions(TranslationOptions):
	fields = ('name', 'description', 'slug')



@register(Project)
class ProjectTranslationOptions(TranslationOptions):
	fields = ('name', 'description', 'slug')


@register(ProjectImage)
class ProjectImageTranslationOptions(TranslationOptions):
	fields = ('description',)


@register(GalleryImage)
class GalleryImageTranslationOptions(TranslationOptions):
	fields = ('description',)