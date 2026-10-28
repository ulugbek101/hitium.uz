"""
Replace services and projects with a small set of mock data (DEBUG only).
Run with: python manage.py seed_data
Every run deletes services/projects and recreates the same records, so it is safe to repeat.
Images point to files already in media/, nothing is copied.
"""
from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from app_main.models import Project, ProjectImage, Service, ServiceImage


SERVICES = [
    {
        "name_ru": "Монтаж котельных",
        "name_uz": "Qozonxonalarni montaj qilish",
        "name_en": "Boiler Room Installation",
        "slug_ru": "montazh-kotelnykh",
        "slug_uz": "qozonxonalarni-montaj-qilish",
        "slug_en": "boiler-room-installation",
        "description_ru": "Проектирование и монтаж котельных под ключ: котлы, горелки, насосные группы и автоматика.",
        "description_uz": "Qozonxonalarni kalit topshirish asosida loyihalash va montaj qilish: qozonlar, gorelkalar, nasos guruhlari va avtomatika.",
        "description_en": "Turnkey design and installation of boiler rooms: boilers, burners, pump groups and automation.",
        "header_bg": "10_4H3Zb1r.JPG",
        "images": ["services/6_fcFTyo4.JPG", "services/8_kiGpXcU.JPG"],
    },
    {
        "name_ru": "Водопровод и канализация",
        "name_uz": "Suv ta'minoti va kanalizatsiya",
        "name_en": "Water Supply and Sewerage",
        "slug_ru": "vodoprovod-i-kanalizaciya",
        "slug_uz": "suv-taminoti-va-kanalizatsiya",
        "slug_en": "water-supply-and-sewerage",
        "description_ru": "Монтаж внутренних и наружных сетей водоснабжения и канализации, установка сантехники.",
        "description_uz": "Ichki va tashqi suv ta'minoti hamda kanalizatsiya tarmoqlarini montaj qilish, santexnika o'rnatish.",
        "description_en": "Installation of indoor and outdoor water supply and sewerage networks and sanitary fixtures.",
        "header_bg": "header-bg_uQgv3hm.jpg",
        "images": ["services/2_m5PtMbm.JPG", "services/1_4z5E2j6.JPG"],
    },
]

PROJECTS = [
    {
        "name_ru": "Монтаж теплового пункта для бизнес-центра",
        "name_uz": "Biznes-markaz uchun issiqlik punktini montaj qilish",
        "name_en": "Heating substation for a business centre",
        "slug_ru": "teplovoj-punkt-biznes-centr",
        "slug_uz": "issiqlik-punkti-biznes-markaz",
        "slug_en": "heating-substation-business-centre",
        "description_ru": "Смонтировали насосные группы, распределительные гребёнки и узел учёта тепла.",
        "description_uz": "Nasos guruhlari, taqsimlovchi kollektorlar va issiqlik hisoblagich uzeli o'rnatildi.",
        "description_en": "Installed pump groups, distribution manifolds and a heat metering unit.",
        "finished_date": date(2025, 11, 20),
        "images": ["project-photos/photo_2025-12-05_12-27-51.jpg", "project-photos/photo_2025-12-05_12-27-58.jpg"],
    },
    {
        "name_ru": "Установка чиллеров на кровле торгового центра",
        "name_uz": "Savdo markazi tomiga chillerlar o'rnatish",
        "name_en": "Rooftop chillers for a shopping mall",
        "slug_ru": "chillery-torgovyj-centr",
        "slug_uz": "chillerlar-savdo-markazi",
        "slug_en": "rooftop-chillers-shopping-mall",
        "description_ru": "Подняли чиллеры краном на кровлю, смонтировали трубопроводы холодоснабжения и запустили систему.",
        "description_uz": "Chillerlar kran bilan tomga ko'tarildi, sovuq ta'minoti quvurlari o'rnatildi va tizim ishga tushirildi.",
        "description_en": "Lifted the chillers onto the roof by crane, installed chilled-water piping and commissioned the system.",
        "finished_date": date(2024, 5, 15),
        "images": ["project-photos/Рисунок35.jpg", "project-photos/Рисунок28.jpg"],
    },
]

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1"


class Command(BaseCommand):
    help = "Replace services and projects with mock data (runs only with DEBUG=True)."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("DEBUG=False — looks like production. seed_data runs only with DEBUG=True; nothing was changed.")

        with transaction.atomic():
            Service.objects.all().delete()
            Project.objects.all().delete()

            for order, data in enumerate(SERVICES, start=1):
                fields = {k: v for k, v in data.items() if k != "images"}
                service = Service.objects.create(order=order, **fields)
                ServiceImage.objects.bulk_create(ServiceImage(service=service, image=path) for path in data["images"])

            for data in PROJECTS:
                fields = {k: v for k, v in data.items() if k != "images"}
                project = Project.objects.create(**fields)
                ProjectImage.objects.bulk_create(ProjectImage(project=project, image=path) for path in data["images"])

            User = get_user_model()
            if not User.objects.filter(username=ADMIN_USERNAME).exists():
                User.objects.create_superuser(ADMIN_USERNAME, password=ADMIN_PASSWORD)

        self.stdout.write(self.style.SUCCESS(
            f"✓ Seeded {len(SERVICES)} services, {len(PROJECTS)} projects; superuser {ADMIN_USERNAME} / {ADMIN_PASSWORD}"
        ))
