from urllib.parse import urlparse

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from app_main.sitemaps import SITEMAPS

from django.conf.urls.static import static
from django.conf import settings

from django.shortcuts import redirect
from django.utils.translation import activate


def switch_language(request):
    lang_code = request.POST.get('language', settings.LANGUAGE_CODE)

    valid_codes = [code for code, _ in settings.LANGUAGES]
    if lang_code not in valid_codes:
        lang_code = settings.LANGUAGE_CODE

    activate(lang_code)

    next_url = request.POST.get('next', '/')

    # Prevent open redirect — reject any URL with a scheme or host
    parsed = urlparse(next_url)
    if parsed.scheme or parsed.netloc:
        next_url = '/'

    # Swap the language prefix in the path
    if not next_url.startswith(f'/{lang_code}/'):
        parts = next_url.lstrip('/').split('/', 1)
        remainder = parts[1] if len(parts) > 1 else ''
        next_url = f'/{lang_code}/{remainder}'

    response = redirect(next_url)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /switch-language/",
        "",
        "Sitemap: https://hitium.uz/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('switch-language/', switch_language, name='switch_language'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    path('', include('app_main.urls')),
)
