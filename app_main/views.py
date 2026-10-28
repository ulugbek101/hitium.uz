import requests

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils.html import escape
from django.utils import translation
from django.utils.formats import date_format

from .models import Service, Project, Client, GalleryImage, Review, News


def home_page(request):
    services = Service.objects.order_by('order')
    projects = Project.objects.prefetch_related("project_images")
    clients = Client.objects.all()
    reviews = Review.objects.filter(is_active=True).order_by('id')
    gallery_images = GalleryImage.objects.all()

    context = {
        "home_page": True,
        "reviews": reviews,
        "services": services,
        "projects": projects,
        "clients": clients,
        "gallery_images": gallery_images,
    }
    return render(request, "app_main/index2.html", context)


def service_detail(request, slug, id):
    services = Service.objects.order_by('order')
    service = get_object_or_404(Service, Q(slug=slug) | Q(id=id))

    context = {
        "services": services,
        "service": service,
        "service_detail": True,
    }
    return render(request, "app_main/service_detail.html", context)


def project_detail(request, slug, id):
    project = get_object_or_404(
        Project.objects.prefetch_related("project_images"),
        Q(slug=slug) | Q(id=id)
    )
    services = Service.objects.order_by('order')

    context = {
        "project": project,
        "services": services,
    }
    return render(request, "app_main/project_detail.html", context)


def our_services(request):
    services = Service.objects.order_by('order')

    context = {
        "services": services,
    }
    return render(request, "app_main/our_services.html", context)


def news(request):
    services = Service.objects.order_by('order')
    news_list = list(News.objects.prefetch_related("media"))

    context = {
        "services": services,
        "featured": news_list[0] if news_list else None,
        "news_list": news_list[1:],
    }
    return render(request, "app_main/news.html", context)


def news_detail(request, slug, id):
    news_item = get_object_or_404(News.objects.prefetch_related("media"), id=id)
    services = Service.objects.order_by('order')

    # Every language version, so the in-page switcher can change the text without a reload
    translations = {}
    for code, name in settings.LANGUAGES:
        with translation.override(code):
            translations[code] = {
                "title": getattr(news_item, f"title_{code}") or news_item.title_ru,
                "description": getattr(news_item, f"description_{code}") or news_item.description_ru,
                "date": date_format(news_item.published_date, "j E Y"),
                "captions": [
                    getattr(media, f"description_{code}") or media.description_ru or ""
                    for media in news_item.media.all()
                ],
            }

    context = {
        "news": news_item,
        "services": services,
        "translations": translations,
    }
    return render(request, "app_main/news_detail.html", context)


def contacts(request):
    services = Service.objects.order_by('order')

    context = {
        "services": services,
    }
    return render(request, "app_main/contacts.html", context)


def send_email(request):
    if request.method != "POST":
        return redirect("contacts")

    full_name = request.POST.get('full_name', '').strip()
    phone_number = request.POST.get('phone_number', '').strip()
    address = request.POST.get('address', '').strip()
    service_id = request.POST.get('service_id', '').strip()
    message = request.POST.get('message', '').strip()

    if not full_name or not phone_number or not service_id:
        return redirect("contacts")

    try:
        service_obj = Service.objects.get(id=int(service_id))
    except (Service.DoesNotExist, ValueError, TypeError):
        return redirect("contacts")

    token = settings.TELEGRAM_BOT_TOKEN
    chat_ids = [710661311, 110387856, 412135367]

    text = (
        f"<b>НОВЫЙ ЗАКАЗ | Hitium.uz</b>\n\n"
        f"ФИО: <b>{escape(full_name.title())}</b>\n"
        f"Номер телефона: <b><code>{escape(phone_number)}</code></b>\n"
        f"Сообщение: <i>{escape(message)}</i>\n\n"
        f"Адрес: <b>{escape(address)}</b>\n"
        f"Тип услуги: <b>{escape(service_obj.name_ru or service_obj.name)}</b>"
    )

    api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    for chat_id in chat_ids:
        try:
            requests.post(
                api_url,
                json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
                timeout=5,
            )
        except requests.RequestException:
            pass

    return redirect("contacts")
