from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=250, verbose_name='слаг')
    description = models.TextField(verbose_name='Описание')
    header_bg = models.ImageField(null=True, verbose_name='Задний фон для шапки')
    description_bg = models.ImageField(null=True, verbose_name='Задний фон для описания')

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = "Сервис"
        verbose_name_plural = "Сервисы"


class ServiceImage(models.Model):
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='services/', verbose_name='Изображение выполненных работ')

    def __str__(self):
        return f'{self.service.name} - {self.image.name}'


    class Meta:
        verbose_name = 'Пример выполненной работы'
        verbose_name_plural = 'Примеры выполненых работ'
