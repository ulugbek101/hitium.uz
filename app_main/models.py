from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    header_bg = models.ImageField(null=True)
    description_bg = models.ImageField(null=True)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = "Сервис"
        verbose_name_plural = "Сервисы"


class ServiceImage(models.Model):
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return f'{self.service.name} - {self.image.name}'
