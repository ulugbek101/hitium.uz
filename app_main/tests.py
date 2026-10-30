from datetime import date

from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import translation

from .models import Client, News, Project, Review, Service
from .templatetags.bento import BIG, HERO, bento_spans, featured_bento_spans
from .views import HOME_SECTION_SIZE

# Home page sections that are left out while they have nothing to show
SECTIONS = ("services", "reviews", "projects", "clients", "news")


def tile_size(span, desktop):
    """(columns, rows) a tile takes on mobile or, with the lg: classes applied, on desktop."""
    size = {"col": 1, "row": 1}
    for cls in sorted(span.split(), key=lambda cls: cls.startswith("lg:")):
        if cls.startswith("lg:") and not desktop:
            continue
        axis, _, count = cls.removeprefix("lg:").rpartition("-span-")
        size[axis] = int(count)
    return size["col"], size["row"]


def area(row, col, width, height):
    return {(row + dr, col + dc) for dr in range(height) for dc in range(width)}


def place(spans, columns, desktop):
    """Cells taken by the tiles when CSS grid auto-places them row by row, as the browser does."""
    taken = set()
    row = col = 0
    for span in spans:
        width, height = tile_size(span, desktop)
        while col + width > columns or area(row, col, width, height) & taken:
            col += 1
            if col + width > columns:
                row, col = row + 1, 0
        taken |= area(row, col, width, height)
        col += width
    return taken


class BentoLayoutTests(SimpleTestCase):
    def assert_no_holes(self, spans):
        for columns, desktop in ((2, False), (4, True)):
            taken = place(spans, columns, desktop)
            rows = max((r for r, _ in taken), default=-1) + 1
            self.assertEqual(taken, {(r, c) for r in range(rows) for c in range(columns)},
                             f"{len(spans)} tiles leave holes in the {columns}-column grid")

    def test_featured_fills_whole_rows_for_any_count(self):
        for count in range(41):
            spans = featured_bento_spans(count)
            self.assertEqual(len(spans), count)
            self.assert_no_holes(spans)

    def test_featured_first_tile_is_big(self):
        for count in range(1, 41):
            self.assertIn(featured_bento_spans(count)[0], (BIG, HERO))

    def test_bento_fills_whole_rows_from_five(self):
        for count in range(5, 41):
            self.assert_no_holes(bento_spans(count))


def create_services(count):
    return [Service.objects.create(name=f"Service {i}", slug=f"service-{i}", description="Text", order=i) for i in range(count)]


def create_reviews(count):
    return [Review.objects.create(fullname=f"Reviewer {i}", video=f"videos/review-{i}.mp4") for i in range(count)]


def create_projects(count):
    return [
        Project.objects.create(name=f"Project {i}", slug=f"project-{i}", description="Text", finished_date=date(2026, 1, i + 1))
        for i in range(count)
    ]


def create_news(count):
    return [
        News.objects.create(title=f"News {i}", slug=f"news-{i}", description="Text", published_date=date(2026, 1, i + 1))
        for i in range(count)
    ]


# Home page sections with a page of their own:
# (page, "see all" button, factory, what a tile links to, which of the factory's items the home page leaves out first)
SECTION_PAGES = {
    "services": ("our_services", "Смотреть все услуги", create_services,
                 lambda s: reverse("service_detail", kwargs={"slug": s.slug, "id": s.id}), -1),
    "reviews": ("reviews", "Смотреть все отзывы", create_reviews, lambda r: r.video.url, 0),
    "projects": ("projects", "Смотреть все проекты", create_projects,
                 lambda p: reverse("project_detail", kwargs={"slug": p.slug, "id": p.id}), 0),
    "news": ("news", "Смотреть все новости", create_news,
             lambda n: reverse("news_detail", kwargs={"slug": n.slug, "id": n.id}), 0),
}


class PageTestCase(TestCase):
    def setUp(self):
        # URLs are reversed with the default "ru-RU" otherwise, and there are no pages under /ru-RU/
        translation.activate("ru")
        self.addCleanup(translation.deactivate)


class HomePageTests(PageTestCase):
    def test_empty_sections_hidden(self):
        response = self.client.get(reverse("home_page"))
        for section in SECTIONS:
            self.assertNotContains(response, f'id="{section}"')

    def test_sections_with_content_shown(self):
        for _, _, create, _, _ in SECTION_PAGES.values():
            create(1)
        Client.objects.create(name="Client", image="client-photos/client.png")
        response = self.client.get(reverse("home_page"))
        for section in SECTIONS:
            self.assertContains(response, f'id="{section}"')

    def test_sections_up_to_limit_show_all_without_button(self):
        for section, (_, label, create, target, _) in SECTION_PAGES.items():
            with self.subTest(section):
                items = create(HOME_SECTION_SIZE)
                response = self.client.get(reverse("home_page"))
                for item in items:
                    self.assertContains(response, target(item))
                self.assertNotContains(response, label)

    def test_sections_over_limit_show_button(self):
        for section, (_, label, create, target, left_out) in SECTION_PAGES.items():
            with self.subTest(section):
                items = create(HOME_SECTION_SIZE + 1)
                response = self.client.get(reverse("home_page"))
                self.assertEqual(len(response.context[f"home_{section}"]), HOME_SECTION_SIZE)
                self.assertNotContains(response, target(items[left_out]))
                self.assertContains(response, label)


class SectionPageTests(PageTestCase):
    def test_pages_show_all_items(self):
        for section, (page, _, create, target, _) in SECTION_PAGES.items():
            with self.subTest(section):
                items = create(HOME_SECTION_SIZE + 3)
                response = self.client.get(reverse(page))
                for item in items:
                    self.assertContains(response, target(item))

    def test_empty_pages_say_so(self):
        for page, text in (("our_services", "Услуги пока не добавлены"), ("reviews", "Отзывов пока нет"),
                           ("projects", "Проекты пока не добавлены"), ("news", "Новостей пока нет")):
            with self.subTest(page):
                self.assertContains(self.client.get(reverse(page)), text)
