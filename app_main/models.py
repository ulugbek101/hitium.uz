from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        abstract = True


class Service(BaseModel):
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=250, verbose_name="Слаг")
    description = models.TextField(verbose_name="Описание")
    header_bg = models.ImageField(null=True, verbose_name="Задний фон для шапки")
    description_bg = models.ImageField(null=True, verbose_name="Задний фон для описания")

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = "Сервис"
        verbose_name_plural = "Сервисы"


class ServiceImage(BaseModel):
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, related_name="service_images")
    image = models.ImageField(upload_to='services/', verbose_name='Изображение выполненных работ')

    def __str__(self):
        return f'{self.service.name} - {self.image.name}'

    class Meta:
        verbose_name = 'Изображение выполненных работ'
        verbose_name_plural = 'Изображения'


class Project(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Название проекта")
    slug = models.SlugField(max_length=250, verbose_name="Слаг")
    description = models.TextField(verbose_name="Описание (что было сделано)")
    finished_date = models.DateField(verbose_name="Когда это было сделано")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class ProjectImage(BaseModel):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, verbose_name="Проект", related_name="project_images")
    image = models.ImageField(upload_to="project-photos/", verbose_name="Фото")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)

    def __str__(self):
        return self.project.name

    class Meta:
        verbose_name = "Фото проект"
        verbose_name_plural = "Фото проектов"


class Client(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Название организации")
    link = models.URLField(verbose_name="Ссылка на сайт организации", null=True, blank=True, help_text="Введите адрес сайта организации (Не обязательно)")
    image = models.ImageField(upload_to="client-photos/", verbose_name="Фото")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class GalleryImage(models.Model):
    image = models.ImageField(upload_to="gallery-photos/", verbose_name="Фото")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Фото галлереи"
        verbose_name_plural = "Фото галлереи"


class Review(BaseModel):
    RATING_CHOICES = [
        [1, "⭐️"],
        [2, "⭐️⭐️"],
        [3, "⭐️⭐️⭐️"],
        [4, "⭐️⭐️⭐️⭐️"],
        [5, "⭐️⭐️⭐️⭐️⭐️"],
    ]

    fullname = models.CharField(max_length=100, verbose_name="ФИО")
    text = models.TextField(verbose_name="Отзыв")
    rating = models.IntegerField(default=5, choices=RATING_CHOICES)
    contacts = models.CharField(max_length=100, verbose_name="Контакты", help_text="Telegram username, Номер телефона, E-mail, ...", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Показывать отзыв ?")

    def __str__(self):
        return f"{self.fullname} - {self.get_rating_display()} - {self.created}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
