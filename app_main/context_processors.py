import datetime
from django.conf import settings
from django.utils.translation import get_language_info, get_language


def global_variables(request):
    language_info = get_language_info(get_language())
    code = language_info['code']
    # Each language is named in itself ("Русский", "O‘zbekcha", "English") whatever the page language
    full_language_name = dict(settings.LANGUAGES).get(code, language_info['name_local'])

    language_flags = {
        "ru": "🇷🇺",
        "uz": "🇺🇿",
        "en": "🇺🇸",
    }

    context = {
        "full_language_name": full_language_name,
        "language_flags": language_flags,
        "current_language_flag": language_flags.get(code),
        "current_year": datetime.date.today().year,
    }
    return context
