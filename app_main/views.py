from django.shortcuts import render
from django.utils.translation import get_language_info, get_language


def home_page(request):
    language_info = get_language_info(get_language())
    code = language_info['code']
    full_language_name = language_info['name_translated']
    language_flags = {
        "ru": "🇷🇺",
        "uz": "🇺🇿",
        "en": "🇺🇸",
    }

    context = {
        "home_page": True,
        "full_language_name": full_language_name,
        "language_flags": language_flags,
        "current_language_flag": language_flags.get(code),
    }
    return render(request, "app_main/index.html", context)
