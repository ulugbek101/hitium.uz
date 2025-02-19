from django.shortcuts import render, redirect
from django.utils.translation import get_language_info, get_language
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

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


def send_email(request):
    if request.method != "POST":
        return redirect("contacts")

    full_name = request.POST.get('full_name')
    address = request.POST.get('address')
    phone_number = request.POST.get('phone_number')
    service_id = request.POST.get('service_id')
    message = request.POST.get('message')

    service_name = Service.objects.get(id=service_id).name_ru


    html_message = render_to_string('email_template.html', {
        'full_name': full_name,
        'address': address,
        'phone_number': phone_number,
        'service_name': service_name,
        'message': message,
    })

    send_mail(
        subject="НОВЫЙ ЗАКАЗ | Hitium.uz",
        message="",
        recipient_list=["ulugbek.programmer02@gmail.com"],
        fail_silently=False,
        from_email=settings.DEFAULT_FROM_EMAIL,
        html_message=html_message,
    )
    return redirect("contacts")
