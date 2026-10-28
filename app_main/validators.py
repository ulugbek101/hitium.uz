from pathlib import Path

from django.core.exceptions import ValidationError

IMAGE_EXTENSIONS = ("jpg", "jpeg", "png", "webp")
VIDEO_EXTENSIONS = ("mp4", "webm", "mov")
NEWS_VIDEO_MAX_MB = 10


def validate_video_size(value):
    limit = 20 * 1024 * 1024  # 20 MB
    if value.size > limit:
        raise ValidationError("Размер видео не должен превышать 20 MB.")


def validate_news_media(value):
    extension = Path(value.name).suffix.lower().lstrip(".")
    if extension not in IMAGE_EXTENSIONS + VIDEO_EXTENSIONS:
        raise ValidationError(
            f"Файл «{Path(value.name).name}» не поддерживается. "
            "Загрузите фото (JPG, PNG, WebP) или видео (MP4, WebM, MOV)."
        )
    if extension in VIDEO_EXTENSIONS and value.size > NEWS_VIDEO_MAX_MB * 1024 * 1024:
        raise ValidationError(
            f"Видео «{Path(value.name).name}» слишком большое: {value.size / 1024 / 1024:.1f} MB. "
            f"Максимальный размер видео — {NEWS_VIDEO_MAX_MB} MB. Сожмите или обрежьте видео и загрузите снова."
        )
