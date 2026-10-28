from django.db import models
from .validators import NEWS_VIDEO_MAX_MB, VIDEO_EXTENSIONS, validate_news_media, validate_video_size


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        abstract = True


class Service(BaseModel):
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=250, verbose_name="Слаг")
    description = models.TextField(verbose_name="Описание")
    header_bg = models.ImageField(null=True, blank=True, verbose_name="Задний фон для шапки")
    description_bg = models.ImageField(null=True, blank=True, verbose_name="Задний фон для описания")
    order = models.IntegerField(default=1, verbose_name="Порядок", help_text="Порядок показа услуги в списке услуг")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сервис"
        verbose_name_plural = "Сервисы"
        ordering = ['order']


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


class GalleryImage(BaseModel):
    image = models.ImageField(upload_to="gallery-photos/", verbose_name="Фото")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Фото галлереи"
        verbose_name_plural = "Фото галлереи"


class Review(BaseModel):
    fullname = models.CharField(max_length=100, verbose_name="Название организации")
    video = models.FileField(
        verbose_name="Видео",
        help_text="Видео отзыв клиента (не больше 20 MB)",
        upload_to="videos/",
        null=True,
        validators=[validate_video_size],
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Показывать отзыв ?",
        help_text="Если отключить, то отзыв не будет показываться. Вместо удаления можно просто отключить видимость",
    )

    def __str__(self):
        return f"{self.fullname} - {self.created.strftime('%d.%m.%Y %H:%M')}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class News(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=250, verbose_name="Слаг")
    description = models.TextField(verbose_name="Текст новости", help_text="Абзацы разделяйте пустой строкой")
    published_date = models.DateField(verbose_name="Дата публикации")
    priority = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Приоритет",
        help_text="Чем меньше число, тем выше новость в списке (1 — большая карточка вверху). "
                  "Без приоритета новости сортируются по дате публикации",
    )

    @property
    def cover(self):
        """First photo of the news, used as the hero background."""
        return next((media for media in self.media.all() if not media.is_video), None)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = [models.F('priority').asc(nulls_last=True), '-published_date', '-created']


class NewsMedia(BaseModel):
    news = models.ForeignKey(to=News, on_delete=models.CASCADE, verbose_name="Новость", related_name="media")
    file = models.FileField(
        upload_to="news/",
        verbose_name="Фото или видео",
        help_text=f"Фото: JPG, PNG, WebP. Видео: MP4, WebM, MOV — не больше {NEWS_VIDEO_MAX_MB} MB",
        validators=[validate_news_media],
    )
    description = models.TextField(verbose_name="Описание", null=True, blank=True)

    @property
    def is_video(self):
        return self.file.name.lower().endswith(VIDEO_EXTENSIONS)

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = "Медиафайл новости"
        verbose_name_plural = "Фото и видео"
        ordering = ['id']
