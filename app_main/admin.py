from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Service, ServiceImage, Project, ProjectImage, Client, GalleryImage, Review


class ImageInline(admin.TabularInline):
    model = ServiceImage    # Make sure ServiceImage is the correct model here
    extra = 1               # Number of empty forms to display


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ImageInline]


# Register Service model with the custom admin class
admin.site.unregister(Group)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(Client)
admin.site.register(GalleryImage)
admin.site.register(Review)

admin.site.site_header = "Административный панель Hitium.uz"
admin.site.site_title = "Добро пожаловать в админ панель Hitium.uz"
admin.site.index_title = "Добро пожаловать в админ панель !"

# No need to register ImageInline explicitly
