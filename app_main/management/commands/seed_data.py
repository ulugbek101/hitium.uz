"""
Replace services, projects, news, reviews and clients with a small set of mock data (DEBUG only).
Run with: python manage.py seed_data
Every run deletes services/projects/news/reviews/clients and recreates the same records, so it is safe to repeat.
Images point to files already in media/, nothing is copied.
"""
from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from app_main.models import Client, News, NewsMedia, Project, ProjectImage, Review, Service, ServiceImage


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
    {
        "name_ru": "Монтаж промышленного оборудования",
        "name_uz": "Sanoat uskunalarini montaj qilish",
        "name_en": "Industrial Equipment Installation",
        "slug_ru": "montazh-promyshlennogo-oborudovaniya",
        "slug_uz": "sanoat-uskunalarini-montaj-qilish",
        "slug_en": "industrial-equipment-installation",
        "description_ru": "Монтаж и пусконаладка технологических линий, ёмкостей и трубопроводов для пищевых и производственных предприятий.",
        "description_uz": "Oziq-ovqat va ishlab chiqarish korxonalari uchun texnologik liniyalar, sig‘imlar va quvurlarni montaj qilish hamda ishga tushirish.",
        "description_en": "Installation and commissioning of process lines, tanks and piping for food and manufacturing plants.",
        "header_bg": "01-montazg-prom-oborudovaniy.jpg",
        "images": ["photo_2025-08-16_20-27-20.jpg", "project-photos/photo_2025-12-05_11-58-05.jpg"],
    },
    {
        "name_ru": "Вентиляция бассейнов",
        "name_uz": "Basseynlar ventilyatsiyasi",
        "name_en": "Pool Ventilation",
        "slug_ru": "ventilyaciya-basseynov",
        "slug_uz": "basseynlar-ventilyatsiyasi",
        "slug_en": "pool-ventilation",
        "description_ru": "Системы вентиляции и осушения воздуха для бассейнов: без конденсата, сырости и запаха хлора.",
        "description_uz": "Basseynlar uchun ventilyatsiya va havoni quritish tizimlari: kondensat, namlik va xlor hidisiz.",
        "description_en": "Ventilation and dehumidification systems for swimming pools: no condensation, damp or chlorine smell.",
        "header_bg": "16.jpg",
        "images": ["desc-bg.jpg"],
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
    {
        "name_ru": "Монтаж линии розлива на заводе напитков",
        "name_uz": "Ichimliklar zavodida quyish liniyasini montaj qilish",
        "name_en": "Bottling line installation at a beverage plant",
        "slug_ru": "liniya-rozliva-zavod-napitkov",
        "slug_uz": "ichimliklar-zavodida-quyish-liniyasi",
        "slug_en": "bottling-line-beverage-plant",
        "description_ru": "Смонтировали линию розлива, обвязали оборудование трубопроводами из нержавеющей стали и провели пусконаладку.",
        "description_uz": "Quyish liniyasi montaj qilindi, uskunalar zanglamaydigan po‘lat quvurlar bilan ulandi va ishga tushirish-sozlash ishlari bajarildi.",
        "description_en": "Installed the bottling line, connected the equipment with stainless steel piping and commissioned it.",
        "finished_date": date(2025, 12, 5),
        "images": ["project-photos/photo_2025-12-05_11-58-07.jpg", "project-photos/photo_2025-12-05_11-58-08.jpg"],
    },
    {
        "name_ru": "Установка резервуаров из нержавеющей стали",
        "name_uz": "Zanglamaydigan po‘latdan yasalgan rezervuarlarni o‘rnatish",
        "name_en": "Stainless steel tank installation",
        "slug_ru": "rezervuary-iz-nerzhaveyushchej-stali",
        "slug_uz": "zanglamaydigan-polat-rezervuarlar",
        "slug_en": "stainless-steel-tanks",
        "description_ru": "Установили и обвязали резервуары для хранения продукции, выполнили теплоизоляцию и опрессовку.",
        "description_uz": "Mahsulot saqlash rezervuarlari o‘rnatildi va quvurlar bilan ulandi, issiqlik izolyatsiyasi va bosim sinovi bajarildi.",
        "description_en": "Installed and piped product storage tanks, insulated them and ran pressure tests.",
        "finished_date": date(2025, 3, 18),
        "images": ["10.JPG", "123.jpg"],
    },
]

NEWS = [
    {
        "title_ru": "ООО «HITIUM» на международной выставке Aquatherm Tashkent 2026",
        "title_uz": "«HITIUM» MChJ «Aquatherm Tashkent 2026» xalqaro koʻrgazmasida",
        "title_en": "HITIUM LLC at the Aquatherm Tashkent 2026 International Exhibition",
        "slug_ru": "hitium-na-aquatherm-tashkent-2026",
        "slug_uz": "hitium-aquatherm-tashkent-2026-korgazmasida",
        "slug_en": "hitium-at-aquatherm-tashkent-2026",
        "description_ru": (
            "Компания ООО «HITIUM» приняла активное участие в крупнейшем отраслевом событии года — 14-й Международной выставке «Aquatherm Tashkent 2026», проходившей в Ташкенте.\n\n"
            "В рамках экспозиции наша команда представила передовые решения и профессиональные услуги в сфере монтажа технологических линий для пищевой промышленности, оборудования для розлива, а также современных инженерных систем и сантехнического оборудования.\n\n"
            "Выставка стала отличной площадкой для встречи с нашими постоянными партнерами и налаживания новых деловых контактов. Мы провели серию успешных переговоров с отечественными и зарубежными коллегами, обсудили перспективы развития отрасли и презентовали наши реализованные проекты.\n\n"
            "Благодарим всех гостей, клиентов и партнеров, посетивших наш стенд! ООО «HITIUM» продолжает уверенно развиваться, внедряя высокие стандарты качества и надежные технологии в каждом проекте."
        ),
        "description_uz": (
            "«HITIUM» MChJ Toshkent shahrida boʻlib oʻtgan yilning eng yirik sohaviy voqeasi — 14-Xalqaro «Aquatherm Tashkent 2026» koʻrgazmasida faol ishtirok etdi.\n\n"
            "Koʻrgazma doirasida mutaxassislarimiz oziq-ovqat va ichimliklar sanoati uchun texnologik liniyalarni montaj qilish, quyish uskunalarini oʻrnatish hamda zamonaviy muhandislik va santexnika tizimlari boʻyicha ilgʻor yechimlar va xizmatlarni taqdim etdilar.\n\n"
            "Ushbu tadbir amaldagi hamkorlarimiz bilan koʻrishish va yangi ishbilarmonlik aloqalarini oʻrnatish uchun ajoyib maydonga aylandi. Muloqotlar davomida mahalliy va xorijiy mutaxassislar bilan muvaffaqiyatli muzokaralar oʻtkazilib, soha rivojlanish istiqbollari va amalga oshirilgan loyihalarimiz muhokama qilindi.\n\n"
            "Stendimizga tashrif buyurgan barcha mehmonlar, mijozlar va hamkorlarimizga oʻz minnatdorchiligimizni bildiramiz! «HITIUM» MChJ har bir loyihada yuqori sifat standartlari va ishonchli texnologiyalarni joriy etgan holda rivojlanishda davom etmoqda."
        ),
        "description_en": (
            "HITIUM LLC took an active part in the region's premier industry event — the 14th International Exhibition \"Aquatherm Tashkent 2026\", held in Tashkent.\n\n"
            "During the exhibition, our team showcased advanced solutions and engineering services specializing in the installation of food and beverage production lines, bottling equipment, as well as modern HVAC and industrial piping systems.\n\n"
            "The event served as an outstanding platform for engaging with our long-standing partners and establishing valuable new business connections. We held a series of productive meetings with domestic and international industry professionals, discussed current market trends, and presented our key completed projects.\n\n"
            "We express our gratitude to all guests, clients, and partners who visited our booth. HITIUM LLC remains committed to delivering top-tier engineering expertise and reliable industrial solutions."
        ),
        "published_date": date(2026, 10, 27),
        "media": [
            ("photo_2025-12-05_11-58-07.jpg", ("Линия розлива — один из проектов, представленных на стенде", "Quyish liniyasi — stendda taqdim etilgan loyihalardan biri", "A bottling line, one of the projects presented at the booth")),
            ("photo_2025-08-16_20-27-20.jpg", ("Оборудование из нержавеющей стали в нашем портфолио", "Portfoliomizdagi zanglamaydigan po‘latdan yasalgan uskunalar", "Stainless steel equipment from our portfolio")),
            ("videos/7593331-hd_1080_1920_25fps.mp4", ("Видеообзор стенда", "Stendning videosharhi", "Booth video tour")),
        ],
    },
    {
        "title_ru": "HITIUM примет участие в Expo 2027",
        "title_uz": "HITIUM Expo 2027 ko'rgazmasida ishtirok etadi",
        "title_en": "HITIUM to exhibit at Expo 2027",
        "slug_ru": "hitium-expo-2027",
        "slug_uz": "hitium-expo-2027-korgazmasida",
        "slug_en": "hitium-at-expo-2027",
        "description_ru": "Весной 2027 года мы снова представим свои проекты и услуги на выставке в Ташкенте. Приглашаем партнёров и клиентов посетить наш стенд.",
        "description_uz": "2027-yil bahorida Toshkentdagi ko'rgazmada loyihalarimiz va xizmatlarimizni yana taqdim etamiz. Hamkorlar va mijozlarni stendimizga taklif qilamiz.",
        "description_en": "In spring 2027 we will once again present our projects and services at the exhibition in Tashkent. Partners and clients are welcome at our booth.",
        "published_date": date(2026, 10, 15),
        "media": [("project-photos/photo_2025-12-05_11-58-05.jpg", None)],
    },
    {
        "title_ru": "Завершён монтаж чиллеров на кровле торгового центра",
        "title_uz": "Savdo markazi tomida chillerlar montaji yakunlandi",
        "title_en": "Rooftop chiller installation completed at a shopping mall",
        "slug_ru": "montazh-chillerov-zavershen",
        "slug_uz": "chillerlar-montaji-yakunlandi",
        "slug_en": "rooftop-chillers-completed",
        "description_ru": "Команда HITIUM подняла оборудование краном на кровлю, смонтировала трубопроводы холодоснабжения и запустила систему.",
        "description_uz": "HITIUM jamoasi uskunani kran yordamida tomga ko'tardi, sovuq ta'minoti quvurlarini o'rnatdi va tizimni ishga tushirdi.",
        "description_en": "The HITIUM team lifted the equipment onto the roof by crane, installed chilled-water piping and commissioned the system.",
        "published_date": date(2026, 9, 30),
        "media": [("videos/8482296-hd_1080_1920_25fps.mp4", None)],
    },
    {
        "title_ru": "Такелаж крупногабаритного оборудования на промышленном объекте",
        "title_uz": "Sanoat obyektida yirik o‘lchamli uskunalarni takelaj qilish",
        "title_en": "Rigging heavy equipment at an industrial site",
        "slug_ru": "takelazh-krupnogabaritnogo-oborudovaniya",
        "slug_uz": "yirik-uskunalarni-takelaj-qilish",
        "slug_en": "rigging-heavy-equipment",
        "description_ru": "Бригада HITIUM подняла и установила крупногабаритное оборудование с помощью автокрана. Работы прошли точно по графику и без остановки производства.",
        "description_uz": "HITIUM brigadasi avtokran yordamida yirik o‘lchamli uskunalarni ko‘tarib, o‘rnatdi. Ishlar jadval asosida va ishlab chiqarishni to‘xtatmasdan bajarildi.",
        "description_en": "The HITIUM crew lifted heavy equipment into place with a mobile crane. The work kept to schedule and production never stopped.",
        "published_date": date(2026, 8, 20),
        "media": [("bg_6HfoVPd.jpg", None)],
    },
]

REVIEWS = [
    ("Тестовый отзыв 1", "videos/7593331-hd_1080_1920_25fps.mp4"),
    ("Тестовый отзыв 2", "videos/8482296-hd_1080_1920_25fps.mp4"),
    ("Тестовый отзыв 3", "videos/7821796-hd_1080_1920_30fps.mp4"),
    ("Тестовый отзыв 4", "videos/IMG_5127.MOV"),
    ("Тестовый отзыв 5", "videos/6473954-uhd_2160_3840_25fps.mp4"),
]

CLIENTS = [
    ("Hydrolife", "client-photos/1673931457.jpg"),
    ("Musaffo", "client-photos/4b4623190e62.jpg"),
    ("Dinay", "client-photos/article-original.jpg"),
    ("Sayhun", "client-photos/sayhun.png"),
]

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1"


class Command(BaseCommand):
    help = "Replace services, projects, news, reviews and clients with mock data (runs only with DEBUG=True)."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("DEBUG=False — looks like production. seed_data runs only with DEBUG=True; nothing was changed.")

        with transaction.atomic():
            Service.objects.all().delete()
            Project.objects.all().delete()
            News.objects.all().delete()
            Review.objects.all().delete()
            Client.objects.all().delete()

            for order, data in enumerate(SERVICES, start=1):
                fields = {k: v for k, v in data.items() if k != "images"}
                service = Service.objects.create(order=order, **fields)
                ServiceImage.objects.bulk_create(ServiceImage(service=service, image=path) for path in data["images"])

            for data in PROJECTS:
                fields = {k: v for k, v in data.items() if k != "images"}
                project = Project.objects.create(**fields)
                ProjectImage.objects.bulk_create(ProjectImage(project=project, image=path) for path in data["images"])

            for data in NEWS:
                fields = {k: v for k, v in data.items() if k != "media"}
                news = News.objects.create(**fields)
                for path, captions in data["media"]:
                    ru, uz, en = captions or (None, None, None)
                    NewsMedia.objects.create(news=news, file=path, description_ru=ru, description_uz=uz, description_en=en)

            Review.objects.bulk_create(Review(fullname=name, video=path) for name, path in REVIEWS)
            Client.objects.bulk_create(Client(name=name, image=path) for name, path in CLIENTS)

            User = get_user_model()
            if not User.objects.filter(username=ADMIN_USERNAME).exists():
                User.objects.create_superuser(ADMIN_USERNAME, password=ADMIN_PASSWORD)

        self.stdout.write(self.style.SUCCESS(
            f"✓ Seeded {len(SERVICES)} services, {len(PROJECTS)} projects, {len(NEWS)} news, {len(REVIEWS)} reviews, "
            f"{len(CLIENTS)} clients; superuser {ADMIN_USERNAME} / {ADMIN_PASSWORD}"
        ))
