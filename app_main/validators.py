from django.core.exceptions import ValidationError

def validate_video_size(value):
    limit = 20 * 1024 * 1024  # 20 MB
    if value.size > limit:
        raise ValidationError("Размер видео не должен превышать 20 MB.")
