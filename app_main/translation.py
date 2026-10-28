from modeltranslation.translator import register, TranslationOptions
from .models import Service, Project, ProjectImage, GalleryImage, News, NewsMedia


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
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


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')


@register(NewsMedia)
class NewsMediaTranslationOptions(TranslationOptions):
    fields = ('description',)
