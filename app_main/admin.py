from django.contrib import admin
# Ensure ServiceImage is correctly imported
from .models import Service, ServiceImage


class ImageInline(admin.TabularInline):
    model = ServiceImage  # Make sure ServiceImage is the correct model here
    extra = 1  # Number of empty forms to display


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ImageInline]


# Register Service model with the custom admin class
admin.site.register(Service, ServiceAdmin)

admin.site.site_header = "Административный панель Hitium.uz"
admin.site.site_title = "Добро пожаловать в админ панель Hitium.uz"
admin.site.index_title = "Доюро пожаловать в админ панель !"
	

# No need to register ImageInline explicitly
