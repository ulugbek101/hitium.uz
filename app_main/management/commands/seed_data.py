"""
Management command to populate the database with dummy data for all models.
Run with: python manage.py seed_data
Add --clear to wipe existing data first: python manage.py seed_data --clear
"""
import io
import struct
import zlib
from datetime import date

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from app_main.models import Client, GalleryImage, Project, ProjectImage, Review, Service, ServiceImage


def _png(width: int, height: int, r: int, g: int, b: int) -> bytes:
    """Generate a minimal valid PNG in memory without Pillow."""
    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    raw = b"".join(b"\x00" + bytes([r, g, b]) * width for _ in range(height))
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


def _img(name: str, r: int = 80, g: int = 80, b: int = 80, w: int = 400, h: int = 300) -> ContentFile:
    """Return a ContentFile wrapping a small solid-colour PNG."""
    return ContentFile(_png(w, h, r, g, b), name=name)


def _mp4() -> bytes:
    """Return bytes for a minimal (empty) MPEG-4 container — no frames, but parseable."""
    def box(tag: bytes, payload: bytes) -> bytes:
        return struct.pack(">I", 8 + len(payload)) + tag + payload

    ftyp_payload = b"isom" + b"\x00\x00\x02\x00" + b"isom" + b"iso2" + b"avc1" + b"mp41"
    return box(b"ftyp", ftyp_payload) + box(b"moov", b"")


SERVICES = [
    {
        "name_ru": "Вентиляционные системы",
        "name_uz": "Ventilyatsiya tizimlari",
        "name_en": "Ventilation Systems",
        "slug_ru": "ventilyacionnye-sistemy",
        "slug_uz": "ventilyatsiya-tizimlari",
        "slug_en": "ventilation-systems",
        "description_ru": (
            "Проектирование, монтаж и техническое обслуживание систем вентиляции и кондиционирования "
            "для промышленных, коммерческих и жилых объектов. Наши специалисты выполняют весь цикл работ — "
            "от расчёта воздухообмена до пусконаладочных испытаний. Используем оборудование ведущих "
            "мировых производителей и обеспечиваем гарантийное сопровождение."
        ),
        "description_uz": (
            "Sanoat, tijorat va turar-joy ob'ektlari uchun ventilyatsiya va konditsionerlash tizimlarini "
            "loyihalash, montaj qilish va texnik xizmat ko'rsatish. Mutaxassislarimiz barcha ishlarni "
            "havo almashinuvini hisoblashdan tortib ishga tushirish sinovlarigacha amalga oshiradi."
        ),
        "description_en": (
            "Design, installation and maintenance of ventilation and air conditioning systems for industrial, "
            "commercial and residential facilities. Our specialists carry out the full cycle of work — from "
            "airflow calculations to commissioning tests. We use equipment from leading global manufacturers."
        ),
        "order": 1,
        "color": (70, 130, 180),
    },
    {
        "name_ru": "Водоснабжение и канализация",
        "name_uz": "Suv ta'minoti va kanalizatsiya",
        "name_en": "Water Supply and Sewerage",
        "slug_ru": "vodosnabzhenie-i-kanalizaciya",
        "slug_uz": "suv-taminoti-va-kanalizatsiya",
        "slug_en": "water-supply-and-sewerage",
        "description_ru": (
            "Полный комплекс работ по проектированию и монтажу систем холодного и горячего водоснабжения, "
            "ливневой и бытовой канализации. Работаем как с новым строительством, так и с реконструкцией "
            "действующих систем. Применяем трубы и арматуру из нержавеющей стали, полипропилена и HDPE."
        ),
        "description_uz": (
            "Sovuq va issiq suv ta'minoti, yomg'ir va maishiy kanalizatsiya tizimlarini loyihalash va "
            "montaj qilish bo'yicha to'liq ishlar majmui. Yangi qurilish va mavjud tizimlarni "
            "rekonstruksiya qilish bilan ishlаymiz."
        ),
        "description_en": (
            "Full range of design and installation works for cold and hot water supply systems, stormwater "
            "and domestic sewerage. We work with both new construction and reconstruction of existing systems. "
            "We use pipes and fittings made of stainless steel, polypropylene and HDPE."
        ),
        "order": 2,
        "color": (30, 144, 255),
    },
    {
        "name_ru": "Котельное оборудование",
        "name_uz": "Qozonxona uskunalari",
        "name_en": "Boiler Equipment",
        "slug_ru": "kotelnoe-oborudovanie",
        "slug_uz": "qozonxona-uskunalari",
        "slug_en": "boiler-equipment",
        "description_ru": (
            "Монтаж «под ключ» котельных установок всех типов: газовых, паровых, водогрейных. "
            "Выполняем обвязку котлов, монтаж горелочного оборудования, дымовых труб, "
            "автоматики безопасности и систем учёта энергоносителей. Проводим гидравлические испытания "
            "и сдачу систем в эксплуатацию."
        ),
        "description_uz": (
            "Barcha turdagi qozonxona qurilmalarini to'liq tayyor holatda o'rnatish: gaz, bug', "
            "issiqlik qozonlari. Qozonlar bilan birga yonish asboblari, tutun quvurlari, "
            "xavfsizlik avtomatikasi va energiya hisobi tizimlarini montaj qilamiz."
        ),
        "description_en": (
            "Turnkey installation of boiler plants of all types: gas, steam, hot water boilers. "
            "We carry out boiler piping, installation of burner equipment, chimneys, safety automation "
            "and energy metering systems. We perform hydraulic tests and system commissioning."
        ),
        "order": 3,
        "color": (210, 105, 30),
    },
    {
        "name_ru": "Холодильные системы",
        "name_uz": "Sovutish tizimlari",
        "name_en": "Refrigeration Systems",
        "slug_ru": "holodilnye-sistemy",
        "slug_uz": "sovutish-tizimlari",
        "slug_en": "refrigeration-systems",
        "description_ru": (
            "Монтаж и обслуживание промышленных и коммерческих холодильных систем: склады-холодильники, "
            "морозильные камеры, витрины охлаждения. Используем хладагенты с низким ГВП, выполняем "
            "испытание на герметичность и настройку автоматики. Гарантия на все виды работ."
        ),
        "description_uz": (
            "Sanoat va tijorat sovutish tizimlarini montaj qilish va texnik xizmat ko'rsatish: "
            "sovuq omborlar, muzlatgich kameralar, sovutish vitrinlari. Past issiqxona gazi "
            "ko'rsatkichiga ega sovutgichlardan foydalanamiz."
        ),
        "description_en": (
            "Installation and maintenance of industrial and commercial refrigeration systems: cold storage "
            "warehouses, freezer chambers, cooling display cases. We use refrigerants with low GWP, "
            "perform leak testing and automation setup. Warranty on all types of work."
        ),
        "order": 4,
        "color": (0, 191, 255),
    },
]

PROJECTS = [
    {
        "name_ru": "Монтаж системы вентиляции на молочном комбинате",
        "name_uz": "Sut kombinatida ventilyatsiya tizimini o'rnatish",
        "name_en": "Ventilation system installation at dairy plant",
        "slug_ru": "montazh-ventilyacii-molochnyj-kombinat",
        "slug_uz": "ventilyatsiya-sut-kombinati",
        "slug_en": "ventilation-dairy-plant",
        "description_ru": "Спроектировали и смонтировали систему приточно-вытяжной вентиляции производственных цехов площадью 4 200 м². Установлены 6 приточных и 4 вытяжных установки марки Systemair с рекуперацией тепла. Срок выполнения: 45 рабочих дней.",
        "description_uz": "4200 m² ishlab chiqarish sexlari uchun kirish-chiqish ventilyatsiya tizimini loyihalashtirdik va o'rnatdik. Issiqlik rekuperatsiyali 6 ta kirish va 4 ta chiqish Systemair qurilmalari o'rnatildi.",
        "description_en": "Designed and installed a supply and exhaust ventilation system for production workshops with a total area of 4,200 m². Installed 6 supply and 4 exhaust Systemair units with heat recovery. Completion time: 45 working days.",
        "finished_date": date(2024, 5, 15),
        "color": (70, 130, 180),
    },
    {
        "name_ru": "Котельная под ключ для торгового центра",
        "name_uz": "Savdo markazi uchun tayyor qozonxona",
        "name_en": "Turnkey boiler room for shopping centre",
        "slug_ru": "kotelnaya-torgovyj-centr",
        "slug_uz": "qozonxona-savdo-markazi",
        "slug_en": "boiler-room-shopping-centre",
        "description_ru": "Смонтировали газовую котельную мощностью 800 кВт для торгово-развлекательного комплекса. В состав системы входят два конденсационных котла Bosch Condens 7000, насосная группа, автоматика Honeywell и узел учёта газа. Проект реализован в 2023 году.",
        "description_uz": "Savdo-ko'ngilliklar kompleksi uchun 800 kVt quvvatli gaz qozonxonasini o'rnatdik. Tizim tarkibiga ikkita Bosch Condens 7000 kondensatsion qozoni, nasos guruhi, Honeywell avtomatikasi va gaz hisobi tugunlari kiradi.",
        "description_en": "Installed an 800 kW gas boiler room for a shopping and entertainment complex. The system includes two Bosch Condens 7000 condensing boilers, a pump group, Honeywell automation and a gas metering unit. Project completed in 2023.",
        "finished_date": date(2023, 11, 30),
        "color": (210, 105, 30),
    },
    {
        "name_ru": "Холодильный склад для фармацевтической компании",
        "name_uz": "Farmatsevtika kompaniyasi uchun sovuq ombor",
        "name_en": "Cold storage warehouse for pharmaceutical company",
        "slug_ru": "holodilnyj-sklad-farmacevtika",
        "slug_uz": "sovuq-ombor-farmatsevtika",
        "slug_en": "cold-storage-pharmaceutical",
        "description_ru": "Оборудовали холодильный склад площадью 600 м² для хранения лекарственных препаратов при температуре +2…+8°C и -18°C. Установлены агрегаты Bitzer, система мониторинга температуры с GSM-оповещением. Соответствие требованиям GDP.",
        "description_uz": "600 m² maydonga ega dori vositalarini +2…+8°C va -18°C haroratda saqlash uchun sovuq ombor jihozladik. Bitzer agregatlar, GSM xabarnomali harorat monitoringi tizimi o'rnatildi.",
        "description_en": "Equipped a 600 m² cold storage warehouse for storing medicines at +2...+8°C and -18°C. Installed Bitzer aggregates, a temperature monitoring system with GSM notifications. Compliant with GDP requirements.",
        "finished_date": date(2024, 3, 10),
        "color": (0, 191, 255),
    },
]

CLIENTS = [
    ("Uzbek-French Pharma", "https://example.com", (180, 30, 30)),
    ("Tashkent Dairy Plant", "https://example.com", (30, 100, 180)),
    ("Samarkand Textile", None, (80, 160, 80)),
    ("Navoi Mining", "https://example.com", (200, 120, 40)),
    ("Uzbek Railways", "https://uzrailways.uz", (40, 40, 150)),
    ("SamarQand Hotels", None, (150, 80, 150)),
]

REVIEWS = [
    ("Алишер Каримов — Tashkent Food Group",   (80, 50, 20)),
    ("Дилноза Юсупова — UzPharma",             (20, 60, 100)),
    ("Бобур Рашидов — Navoi Cement",           (60, 80, 60)),
]


class Command(BaseCommand):
    help = "Seed the database with realistic dummy data (safe to run multiple times)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing data before seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing data…")
            for model in (Review, ServiceImage, Service, ProjectImage, Project, Client, GalleryImage):
                model.objects.all().delete()
            self.stdout.write(self.style.WARNING("  Cleared."))

        self._seed_services()
        self._seed_projects()
        self._seed_clients()
        self._seed_reviews()
        self.stdout.write(self.style.SUCCESS("✓ Dummy data created successfully."))
        self.stdout.write("  Run 'python manage.py compilemessages' if you haven't already.")

    # ── Services ────────────────────────────────────────────────────────────────
    def _seed_services(self):
        for data in SERVICES:
            color = data.pop("color")
            slug = data["slug_ru"]
            defaults = {k: v for k, v in data.items() if k != "slug_ru"}
            svc, created = Service.objects.update_or_create(slug_ru=slug, defaults=defaults)
            if not svc.header_bg:
                r, g, b = color
                svc.header_bg.save(
                    f"placeholder_{slug}.png",
                    _img(f"{slug}.png", r, g, b, 800, 500),
                    save=False,
                )
                svc.save()
            self._add_service_images(svc, color)
            verb = "Created" if created else "Updated"
            self.stdout.write(f"  {verb} service: {svc.name_ru}")

    def _add_service_images(self, svc: Service, color: tuple):
        if svc.service_images.exists():
            return
        r, g, b = color
        for i in range(3):
            si = ServiceImage(service=svc)
            si.image.save(
                f"svc_{svc.slug_ru}_{i}.png",
                _img(f"svc_{i}.png", min(r + i * 20, 255), g, b, 600, 400),
                save=False,
            )
            si.save()

    # ── Projects ─────────────────────────────────────────────────────────────────
    def _seed_projects(self):
        for data in PROJECTS:
            color = data.pop("color")
            slug = data["slug_ru"]
            defaults = {k: v for k, v in data.items() if k != "slug_ru"}
            proj, created = Project.objects.update_or_create(slug_ru=slug, defaults=defaults)
            self._add_project_images(proj, color)
            verb = "Created" if created else "Updated"
            self.stdout.write(f"  {verb} project: {proj.name_ru}")

    def _add_project_images(self, proj: Project, color: tuple):
        if proj.project_images.exists():
            return
        r, g, b = color
        captions = ["Общий вид", "Оборудование", "Монтаж"]
        for i, caption in enumerate(captions):
            pi = ProjectImage(
                project=proj,
                description=caption,
            )
            pi.image.save(
                f"proj_{proj.slug_ru}_{i}.png",
                _img(f"proj_{i}.png", min(r + i * 15, 255), g, min(b + i * 10, 255), 700, 500),
                save=False,
            )
            pi.save()

    # ── Clients ──────────────────────────────────────────────────────────────────
    def _seed_clients(self):
        for name, link, color in CLIENTS:
            existing = Client.objects.filter(name=name).first()
            if existing:
                existing.link = link
                existing.save()
                self.stdout.write(f"  Updated client: {name}")
                continue
            r, g, b = color
            client = Client(name=name, link=link)
            client.image.save(
                f"client_{name[:10].replace(' ', '_')}.png",
                _img(f"client.png", r, g, b, 200, 100),
                save=False,
            )
            client.save()
            self.stdout.write(f"  Created client: {name}")

    # ── Reviews ──────────────────────────────────────────────────────────────────
    def _seed_reviews(self):
        mp4_bytes = _mp4()
        for fullname, color in REVIEWS:
            if Review.objects.filter(fullname=fullname).exists():
                self.stdout.write(f"  Review exists: {fullname}")
                continue
            rev = Review(fullname=fullname, is_active=True)
            rev.video.save(
                f"review_{fullname[:8].replace(' ', '_')}.mp4",
                ContentFile(mp4_bytes, name="review.mp4"),
                save=False,
            )
            rev.save()
            self.stdout.write(f"  Created review: {fullname}")
