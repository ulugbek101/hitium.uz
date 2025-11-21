from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django import forms

from unfold.admin import ModelAdmin

from .models import Service, ServiceImage, Project, ProjectImage, Client, GalleryImage, Review

admin.site.unregister(Group)
admin.site.unregister(User)


UNFOLD_INPUT_CLASSES = (
    "border border-base-200 bg-white font-medium min-w-20 placeholder-base-400 rounded-default shadow-xs "
    "text-font-default-light text-sm focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 "
    "group-[.errors]:border-red-600 focus:group-[.errors]:outline-red-600 dark:bg-base-900 dark:border-base-700 "
    "dark:text-font-default-dark dark:group-[.errors]:border-red-500 dark:focus:group-[.errors]:outline-red-500 "
    "dark:scheme-dark group-[.primary]:border-transparent disabled:!bg-base-50 dark:disabled:!bg-base-800 px-3 "
    "py-2 w-full max-w-2xl "
)


# User change form
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


# User creation form
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": UNFOLD_INPUT_CLASSES})


@admin.register(User)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ("name",)
    inlines = [ServiceImageInline]


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    inlines = [ProjectImageInline]


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    ...


@admin.register(GalleryImage)
class GalleryImageAdmin(ModelAdmin):
    ...


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    ...


admin.site.site_header = "Административный панель Hitium.uz"
admin.site.site_title = "Добро пожаловать в админ панель Hitium.uz"
admin.site.index_title = "Добро пожаловать в админ панель !"
