from django.db import models


class MediaFile(models.Model):
    """Модель для хранения информации о медиа файлах"""
    MEDIA_TYPES = [
        ('avatar', 'Аватар'),
        ('post_image', 'Изображение поста'),
    ]

    original_url = models.URLField(verbose_name='URL оригинала')
    thumbnail_url = models.URLField(blank=True, null=True, verbose_name='URL миниатюры')
    small_url = models.URLField(blank=True, null=True, verbose_name='URL маленькой версии')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, verbose_name='Тип медиа')
    processing = models.BooleanField(default=False, verbose_name='Обработка')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Медиа файл'
        verbose_name_plural = 'Медиа файлы'

