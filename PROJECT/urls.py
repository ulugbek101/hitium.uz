from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from django.conf.urls.static import static
from django.conf import settings

from django.shortcuts import redirect
from django.utils.translation import activate, get_language


def switch_language(request):
    lang_code = request.POST.get(
        'language', settings.LANGUAGE_CODE)  # Default to 'ru'
    activate(lang_code)

    # Get the next URL or fallback to the home page
    next_url = request.POST.get('next', '/')

    # Ensure the language prefix is included in the URL
    if not next_url.startswith(f'/{lang_code}/'):
        next_url = f'/{lang_code}{next_url[3:]}'

    response = redirect(next_url)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response



urlpatterns = [
    path('admin/', admin.site.urls),
    path('switch-language/', switch_language, name='switch_language'),
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    path('', include('app_main.urls')),
)

