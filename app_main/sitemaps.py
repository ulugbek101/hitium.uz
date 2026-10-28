from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import News, Project, Service


class I18nSitemap(Sitemap):
    """Lists every URL in all site languages with hreflang alternates."""
    i18n = True
    alternates = True
    protocol = "https"

    def images(self, obj):
        """Photos of the item, listed in the image sitemap."""
        return []

    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page, site, protocol)
        for url in urls:
            obj, _lang = url["item"]
            origin = "/".join(url["location"].split("/")[:3])
            url["images"] = [origin + image.url for image in self.images(obj)]
        return urls


class StaticPagesSitemap(I18nSitemap):
    changefreq = "weekly"

    def items(self):
        return ["home_page", "our_services", "news", "contacts"]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(I18nSitemap):
    changefreq = "monthly"

    def items(self):
        return Service.objects.prefetch_related("service_images").order_by("order")

    def location(self, obj):
        return reverse("service_detail", kwargs={"slug": obj.slug, "id": obj.id})

    def lastmod(self, obj):
        return obj.updated

    def images(self, obj):
        header = [obj.header_bg] if obj.header_bg else []
        return header + [img.image for img in obj.service_images.all()]


class ProjectSitemap(I18nSitemap):
    changefreq = "monthly"

    def items(self):
        return Project.objects.prefetch_related("project_images").order_by("-finished_date")

    def location(self, obj):
        return reverse("project_detail", kwargs={"slug": obj.slug, "id": obj.id})

    def lastmod(self, obj):
        return obj.updated

    def images(self, obj):
        return [img.image for img in obj.project_images.all()]


class NewsSitemap(I18nSitemap):
    changefreq = "weekly"

    def items(self):
        return News.objects.prefetch_related("media")

    def location(self, obj):
        return reverse("news_detail", kwargs={"slug": obj.slug, "id": obj.id})

    def lastmod(self, obj):
        return obj.updated

    def images(self, obj):
        return [media.file for media in obj.media.all() if not media.is_video]


SITEMAPS = {
    "pages": StaticPagesSitemap,
    "services": ServiceSitemap,
    "projects": ProjectSitemap,
    "news": NewsSitemap,
}
