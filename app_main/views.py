import datetime
import requests

from django.shortcuts import render, redirect
from django.db.models import Q

from .models import Service, Project, Client, GalleryImage, Review


def home_page(request):
    services = Service.objects.all()
    projects = Project.objects.prefetch_related("project_images")
    clients = Client.objects.all()
    reviews = Review.objects.filter(is_active=True)
    gallery_images = GalleryImage.objects.all()

    context = {
        "home_page": True,
        "reviews": reviews,
        "services": services,
        "projects": projects,
        "clients": clients,
        "gallery_images": gallery_images,
        "current_year": datetime.date.today().year,
    }
    # return render(request, "app_main/index.html", context)
    return render(request, "app_main/index2.html", context)


def service_detail(request, slug, id):
    services = Service.objects.all()
    service = services.get(Q(slug=slug) | Q(id=id))

    context = {
        "services": services,
        "service": service,
        "service_detail": True,
    }
    return render(request, "app_main/service_detail.html", context)


def project_detail(request, slug, id):
    project = Project.objects.prefetch_related("project_images").get(
        Q(slug=slug) |
        Q(id=id)
    )
    services = Service.objects.all()

    context = {
        "project": project,
        "services": services,
    }
    return render(request, "app_main/project_detail.html", context)


def our_services(request):
    services = Service.objects.all()

    context = {
        "services": services,
    }
    return render(request, "app_main/our_services.html", context)


def contacts(request):
    services = Service.objects.all()

    context = {
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
    CHAT_IDS = [710661311, 110387856, 412135367]  # your user's Telegram ID
    service_obj = Service.objects.get(id=service_id)

    text = f"""<b>НОВЫЙ ЗАКАЗ | Hitium.uz</b>

ФИО: <b>{full_name.title()}</b>
Номер телефона: <b><code>{phone_number}</code></b>
Сообщение: <i>{message}</i>

Адрес:      <b>{address}</b>
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

    return redirect("contacts")
