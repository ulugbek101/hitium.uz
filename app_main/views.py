import datetime
import requests

from django.shortcuts import render, redirect
from django.utils.translation import get_language_info, get_language
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .models import Service, Project


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
    projects = Project.objects.prefetch_related("project_images")

    context = {
        "home_page": True,
        "full_language_name": full_language_name,
        "language_flags": language_flags,
        "current_language_flag": language_flags.get(code),
        "services": services,
        "projects": projects,
        "current_year": datetime.date.today().year,
    }
    # return render(request, "app_main/index.html", context)
    return render(request, "app_main/index2.html", context)


def service_detail(request, slug):
    services = Service.objects.all()
    service = services.get(slug=slug)
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


def project_detail(request, slug):
    project = Project.objects.prefetch_related("project_images").get(slug=slug)
    services = Service.objects.all()

    context = {
        "project": project,
        "services": services,
    }
    return render(request, "app_main/project_detail.html", context)


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
    phone_number = request.POST.get('phone_number')
    address = request.POST.get('address')
    service_id = request.POST.get('service_id')
    message = request.POST.get('message')

    TELEGRAM_BOT_TOKEN = "7960992571:AAGjpwEJFvM2fY2iNAnRlLYDRSsONLJ-thQ"
    CHAT_IDS = [710661311, 110387856, ]  # your user's Telegram ID
    service_obj = Service.objects.get(id=service_id)

    text = f"""<b>НОВЫЙ ЗАКАЗ | Hitium.uz</b>

ФИО: <b>{full_name.title()}</b>
Номер телефона: <code>{phone_number}</code>
Сообщение: <i>{message}</i>

Адрес: <code>{address}</code>
Тип услуги: <b>{service_obj.name_ru}</b>
"""


    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    for CHAT_ID in CHAT_IDS:
        try:
            payload = {
                "chat_id": CHAT_ID,
                "text": text,
                "parse_mode": "HTML"
            }
            requests.post(url, json=payload)
        except:
            pass

    # html_message = render_to_string('email_template.html', {
    #     'full_name': full_name,
    #     'phone_number': phone_number,
    #     'message': message,
    # })

    # send_mail(
    #     subject="НОВЫЙ ЗАКАЗ | Hitium.uz",
    #     message="",
    #     recipient_list=["ulugbek.programmer02@gmail.com", "hitiumservice@gmail.com"],
    #     fail_silently=False,
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     html_message=html_message,
    # )
    return redirect("contacts")
