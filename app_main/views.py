from django.shortcuts import render
from django.utils.translation import get_language_info, get_language

from .models import Service


def home_page(request):
    language_info = get_language_info(get_language())
    code = language_info['code']
    full_language_name = language_info['name_translated']
    language_flags = {
        "ru": "🇷🇺",
        "uz": "🇺🇿",
        "en": "🇺🇸",
    }

    services = Service.objects.all()
    context = {
        "home_page": True,
        "full_language_name": full_language_name,
        "language_flags": language_flags,
        "current_language_flag": language_flags.get(code),
        "services": services,
    }
    return render(request, "app_main/index.html", context)


def service_detail(request, slug):
    services = Service.objects.all()
    service = Service.objects.get(slug=slug)
    language_info = get_language_info(get_language())
    code = language_info['code']
    full_language_name = language_info['name_translated']

    language_flags = {
        "ru": "🇷🇺",
        "uz": "🇺🇿",
        "en": "🇺🇸",
    }
    
    context = {
        "services": services,
        "service": service,
        "service_detail": True,
        "full_language_name": full_language_name,
        "language_flags": language_flags,
        "current_language_flag": language_flags.get(code),
    }
    return render(request, "app_main/service_detail.html", context)



def our_services(request):
    language_info = get_language_info(get_language())
    full_language_name = language_info['name_translated']
    services = Service.objects.all()

    context = {
        "full_language_name": full_language_name,
        "services": services,
    }
    return render(request, "app_main/our_services.html", context)


def contacts(request):
    language_info = get_language_info(get_language())
    full_language_name = language_info['name_translated']
    services = Service.objects.all()

    context = {
        "full_language_name": full_language_name,
        "services": services,

    }
    return render(request, "app_main/contacts.html", context)
